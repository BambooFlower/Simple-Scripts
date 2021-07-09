% Parameter M adjacency matrix where M_i,j represents the link from 'j' to 'i', such that for all 'j'
%     sum(i, M_i,j) = 1
% Parameter d damping factor
% Parameter v_quadratic_error quadratic error for v
% Return v, a vector of ranks such that v_i is the i-th rank from [0, 1]

function [v] = rank2(M, d, v_quadratic_error)

N = size(M, 2); % N is equal to either dimension of M and the number of documents
v = rand(N, 1);
v = v ./ norm(v, 1);   % This is now L1, not L2
last_v = ones(N, 1) * inf;
M_hat = (d .* M) + (((1 - d) / N) .* ones(N, N));

while (norm(v - last_v, 2) > v_quadratic_error)
	last_v = v;
	v = M_hat * v;
        % removed the L2 norm of the iterated PR
end

end 