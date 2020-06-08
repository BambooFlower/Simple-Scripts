classdef BTree
% Create a Binary Tree from a given list, the created tree is then searchable
% 
% Example: BTree([1,2,3,4,5,6,7,8])
   
    properties
        value
        left
        right
    end
    
    methods
        function t = BTree(x)
            % 2 cases
            % - input is single value: create singleton tree
            if all( size(x) == 1 )
                t.value = x;
                t.left  = [];
                t.right = [];
            % - input is array: create tree with given values
            elseif all( size(x) ~= 0 )
                t = fromArray(x); 
            end
            
            % Inner function to build tree
            function t = fromArray(A)
                
                % Catch n-dimensional arrays by casting to 1 dimension
                A = A(:);
                
                % Create singleton tree from first value
                t = BTree(A(1));
                
                % Insert remaining values into tree
                for i = 2:length(A)
                    t = t.insert(A(i));
                end
            end
        end
     
        % Ignore this - it's a mess but it works. 
        function disp(t)
            disp(format(t,' ',' '))
            disp(newline)
            
            function s = format(t,c,d)
                r = [];
                l = [];
                if ~isempty(t.left)
                    l = format(t.left,' ','-');
                    l = [ l , [ '-' ; ' ' ; zeros(size(l,1)-2,1) + ' ' ] ];
                end
                if ~isempty(t.right)
                    r = format(t.right,'-',' ');
                    r = [ [ '-' ; ' ' ; zeros(size(r,1)-2,1) + ' ' ] , r ];
                end
                v = num2str(t.value);
                [yl,xl] = size(l);
                [yc,xc] = size(v);
                [yr,xr] = size(r);
                x = xl + xc + xr;
                y = max([yl,yr,yc]);
                s = [ [ zeros(2,xl) + ' ' ; l ; zeros(y-yl,xl) + ' ' ] , ...
                      [ zeros(2,xc) + ' ' ; v ; zeros(y-yc,xc) + ' ' ] , ...
                      [ zeros(2,xr) + ' ' ; r ; zeros(y-yr,xr) + ' ' ] ];
                i = xl + ceil((xc+1)/2);
                s(1:2,i)   = ['+';'|'];
                s(1,1:i-1) = c;
                s(1,i+1:x) = d;
            end
        end
        
        function b = find(t,x)
            % Default: x not found
            b = false;
            % Use a while-loop, changing target of t to recurse
            while ~isempty(t)
                % 3 cases
                % - x in left  subtree
                % - x in right subtree
                % - x right here
                if     x < t.value 
                    t = t.left;
                elseif t.value < x 
                    t = t.right; 
                else
                    b = true;    
                    return
                end
            end
        end
                
        function t = insert(t,x)
            t = inner(t,x);
            
            % Use inner function for nicer recursion
            function t = inner(t,x)
                % four cases:
                % - t is a leaf: insert x as new tree
                % - x is in left  subtree: recurse
                % - x is in right subtree: recurse
                % - x is right here: do nothing (omitted)
                if     isempty(t) 
                    t = BTree(x);
                elseif x < t.value 
                    t.left  = inner(t.left ,x);
                elseif t.value < x 
                    t.right = inner(t.right,x);
                end
            end
        end
        
        function A = toArray(t)
            A = inner(t);
            
            % Use inner function for nicer recursion
            function A = inner(t)
                if isempty(t)
                    A = [];
                else
                    % Ignore growing array issues for nicer recursion
                    A = [ inner(t.left) , t.value , inner(t.right) ];
                end
            end
        end
        
        function n = max(t)
            if isempty(t.right) == 1
                n = t.value;
            else
                n = max(t.right);
            end
        end
        
        function n = size(t)
            n = inner(t);
            
            function n = inner(t)
                if isempty(t) 
                    n = 0;
                else
                    n = 1 + inner(t.right) + inner(t.left);
                end
            end
        end
        
        function n = height(t)
            n = inner(t);
            
            function n = inner(t)
                if isempty(t)
                    n = 0;
                else
                    a = inner(t.right);
                    b = inner(t.left);
                    if a > b
                        n = a + 1;
                    else
                        n = b + 1;
                    end
                end
            end
            
        end
        
        function t = search(t,x)
            t = inner(t,x);
            
            function t = inner(t,x)
                if isempty(t) 
                    t = 0;
                elseif x < t.value 
                    t = inner(t.left ,x);
                elseif x > t.value
                    t = inner(t.right,x);
                elseif x == t.value
                    t = 1;
                end
            end
            
            t = logical(t);
        end
   
    end    
end


