
c = 24;
a = 10;

c = c + 2;

a = c / (1 + 1);

isPrime = 1;
if mod(a, 2) == 0
    isPrime = 0;
else
    for i = 3:2:sqrt(a)
        if mod(a, i) == 0
            isPrime = 0;
            break;
        end
    end
end

% Display result
if isPrime
    fprintf('%d\n', a);
end
if c > 14
    fprintf('c = %d\n', c);
else
    fprintf('asdf\n');
end
