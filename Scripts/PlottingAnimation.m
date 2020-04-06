% Plotting animation template for MATLAB

clear
close all

h = animatedline;
axis([0,4*pi,-1,1])
title('Plotting animation of y = sin(x)')
xlabel('x')
ylabel('y')
grid on

x = linspace(0,4*pi,1000);
y = sin(x);
for k = 1:length(x)
    addpoints(h,x(k),y(k));
    drawnow 
end


