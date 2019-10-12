int main(){
    _Atomic(int) a = 2;
    auto b = 3;
    int c, d = 4;

    int * const volatile c = a*b;
    int d = c/b;
    int e = d%c;

    int f = a+b;
    int g = d-e;

    int h = g<<4;
    int i = h>>20;

    int j = i--;
    return 0;
}