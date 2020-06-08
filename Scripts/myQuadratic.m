% The program takes 3 inputs a,b and c and either computes the solutions to
% the quadratic ax^2+bx+c or a message that the solutions are not real

a = input('Enter a value for a: ');
b = input('Enter a value for b: ');
c = input('Enter a value for c: ');

x1 = (-b + sqrt(((b^2) - 4*a*c)))/(2*a);
x2 = (-b - sqrt(((b^2) - 4*a*c)))/(2*a);

test1 = isreal(x1);
test2 = isreal(x2);

if (test1 == 0 || test2 == 0)
    disp('The solutions are not real')
elseif x1 == x2
    disp("The only solution is: " + x1)
else
    disp("One solution is: " + x1)
    disp("And the other is: " + x2)
end
