
c = 24;
a = 10;
x = "String";
disp(x);
disp("HELLO");
a = a +1;
c = c + 2;
a = c / (1 + 1);

isPrime = 1;
if mod(a, 2) == 0
    isPrime = 0;
else
    for i = 3:2:a
        if mod(a, i) == 0
            isPrime = 0;
            break;
        end
    end
end

if isPrime
    disp(a);
end
if c > 14
    disp(c);
else
    disp(a);
end
