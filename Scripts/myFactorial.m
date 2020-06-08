% The program takes a number and calculates its factorial value

n = input('Enter a positive integer: ');
result = 1;
if n == 0 || n == 1
    result = 1;
else
    for i = 1:n
        result = i*result;
    end
end

  
disp("The factorial of the number is: " + result)