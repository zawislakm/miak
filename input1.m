% Test comment
test = "Test string";
disp(test);

disp("Pętla for:");
for i = 1:5
    disp(i);
end

disp("Warunek if:");
number_to_check = 7;
if mod(number_to_check, 2) == 0
    disp("Liczba jest parzysta.");
else
    disp("Liczba jest nieparzysta.");
end

disp("Pętla while:");
counter = 1;
while counter <= 5
    disp(counter);
    counter = counter + 1;
    if counter == 3
        disp(counter / 3);
    end

end