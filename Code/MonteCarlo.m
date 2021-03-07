% Monte Carlo approximation of pi using the area of a circle segment
function a = MonteCarlo(n)

% generate n uniformly sampled points in [0, 1]
points = rand(n,2);

% compute the 2-norm squared of each point (x, y)
norms2 = points(:,1).^2 + points(:,2).^2;

% compute how many points lay inside the unit circle (segment)
normsBelow = norms2(norms2<=1); % extract only the points with norm below 1

m = numel(normsBelow);          % number of such elements

% estimate the area of the segment
a = 4*m/n;

end