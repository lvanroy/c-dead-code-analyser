int main(){
    _Atomic(int) a = 2;
    auto b = 3;
    int c, d = 4;
    char* q = "loool";

    int * const volatile c = a*b;
    b = c/b;
    b = d%c;
    b = a + 'c';
    int z = a = d;

    b = a+b+b+c+d;
    b = d-e;

    b = g<<4;
    b = h>>20;

    b = i--;
    return 0;
}