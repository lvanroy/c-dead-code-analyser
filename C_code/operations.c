int main(){
    _Atomic(int) a = 2;
    auto b = 3;
    int c, d = 4;
    char* e = "loool";

    int * const volatile f = a*b;
    b = c/b;
    b = d%d;
    b = a + 'c';
    int g = b = d;

    b = a+b+b+c+d;
    b = d-b;

    b = g<<4;
    b = b>>20;

    b = b--;
    return 0;
}