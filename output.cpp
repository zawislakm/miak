#include <iostream> 
 using namespace std;
int main() {
// Test comment
auto test = "Test string";
cout<<test<<endl;
cout<<"Pętla for:"<<endl;
for(auto i = 1; i <= 5; i ++){
cout<<i<<endl;}

cout<<"Warunek if:"<<endl;
auto number_to_check = 7;
if( number_to_check % 2 == 0){
cout<<"Liczba jest parzysta."<<endl;
}else{
cout<<"Liczba jest nieparzysta."<<endl;
}

cout<<"Pętla while:"<<endl;
auto counter = 1;
while(counter <= 5) {
    cout<<counter<<endl;
    counter = counter + 1;
    if( counter == 3){
cout<<counter / 3<<endl;
}

}

return 0; }
