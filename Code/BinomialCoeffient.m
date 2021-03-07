function y = BinomialCoeffient(alpha, k)
% Computes the binomial coefficient

y = [];

% Check if the inputs are valid
if (alpha~=floor(alpha)) || (k~=floor(k)) || (alpha<0) || (k<0)
    fprintf('alpha and k should be positive integer\n')
    return
end
if alpha < k
    fprintf('alpha should be greater or equal than k\n')
    return
end

% Numerator - use a for loop first
num = alpha;
for i = 1:k-1
    num = num*(alpha-i);
end

% Denominator
den = 1:k; 
den = prod(den); % Similar vectorised operations could be used for num too
y = num/den;

end


