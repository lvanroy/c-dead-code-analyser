int main(){
    // primary initializer
    int a = 0;

    // assignment initializer
    int b = a = 5;

    // conditional initializer
    int c = a == 5 ? 3 : 4;

    // logical or initializer
    int d = 5 || 0;

    // logical and initializer
    int e = 2 && 3;

    // inclusive or initializer
    int f = 2 | 0;

    // exclusive or initializer
    int g = 2 ^ 0;

    // and initializer
    int h = 2 ^ 0 && 5;

    // equality initializer
    int i = 2 == 3;

    // relational initializer
    int j = 2 < 3;

    // shift initializer
    int k = 2 << 2;

    // additive initializer
    int l = a + 5;
    int m = a - b;

    // multiplicative initializer
    int n = b * 2;
    int o = b / 5;
    int p = d % 3;

    // cast initializer
    int q = (int) 5.0;

    // unary initializer
    int s = --a;
    int r = ++a;
    int t = -a;
    int u = ~a;
    int v = !a;
    int w = sizeof(a);

    // postfix initializer
}