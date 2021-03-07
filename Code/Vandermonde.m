function V = Vandermonde(x)
% Computes the Vandermonde matrix of x

if (size(x,2)~=1)
    fprintf('The input should be a column vector\n');
    V = [];
    return
end
n = size(x,1);
jVector = 0:(n-1);
V = x.^jVector; % Note that x must be a column, and jVector must be a row.

end