% The program takes a positive integer n and creates a n*n matrix with 
% (i,j)th component given by A(i,j) = sin(1/(i+j-1))

n = input('Enter a positive integer: ');
A = zeros(n);

for i = 1:n
    for j = 1:n
        A(i,j) = sin(1/((i+j)-1));
    end
end

disp(A)