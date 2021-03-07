% This script compares the Symplectic and Forward Euler methods on the
% simple pendulum problem.

h = input('Enter the step size (e.g. 0.1): ');
alpha = input('Enter the initial angle (e.g. pi/2): ');
T = input('Enter the final time (e.g. 100): ');
method = input('Choose the method (''FE'' or ''SE''): ');

% Number of time steps
N = T/h;

% Potential gradient function
Vp = @(q)sin(q);

% Hamiltonian function
H = @(q,p)p.^2/2 - cos(q);

% Storage for all steps
Q = zeros(1,N+1);
P = zeros(1,N+1);
Q(1) = alpha;

% Choose the method: it's sufficient to look at 1st character of its name
if (strcmpi(method(1), 's'))    % check also help strcmpi
    fprintf('Using the Symplectic Euler method \n');
    for k=1:N
        Q(k+1) = Q(k) + h*P(k);
        P(k+1) = P(k) - h*Vp(Q(k+1));
    end
else
    fprintf('Using the Forward Euler method \n');
    for k=1:N
        P(k+1) = P(k) - h*Vp(Q(k));
        Q(k+1) = Q(k) + h*P(k);
    end
end

% Plot the solution
tk = h*(0:N);
figure(1);
plot(tk, Q, tk, P);
xlabel('t');
legend('Q', 'P');
title(sprintf('Numerical solution for %s', method));

figure(2);
plot(Q,P);
xlabel('Q');
ylabel('P');
title(sprintf('Phase trajectory for %s', method));

figure(3);
plot(tk, H(Q,P))
xlabel('t');
ylabel('H');
title(sprintf('Numerical Hamiltonian for %s', method));



