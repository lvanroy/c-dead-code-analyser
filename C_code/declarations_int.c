#include "stdio.h"

int main(){
    // primary initializer
    int a = 0;
    printf("%d \n", a);

    // assignment initializer
    int b = a = 5;
    printf("%d \n", b);

    // conditional initializer
    int c = a == 5 ? 3 : 4;
    printf("%d \n", c);

    // logical or initializer
    int d = 5 || 0;
    printf("%d \n", d);

    // logical and initializer
    int e = 2 && 3;
    printf("%d \n", e);

    // inclusive or initializer
    int f = 2 | 0;
    printf("%d \n", f);

    // exclusive or initializer
    int g = 2 ^ 0;
    printf("%d \n", g);

    // and initializer
    int h = 2 ^ 0 && 5;
    printf("%d \n", h);

    // equality initializer
    int i = 2 == 3;
    printf("%d \n", i);

    // relational initializer
    int j = 2 < 3;
    printf("%d \n", j);

    // shift initializer
    int k = 2 << 2;
    printf("%d \n", k);

    // additive initializer
    int l = a + 5;
    printf("%d \n", l);
    int m = a - b;
    printf("%d \n", m);

    // multiplicative initializer
    int n = b * 2;
    printf("%d \n", n);
    int o = b / 5;
    printf("%d \n", o);
    int p = d % 3;
    printf("%d \n", p);

    // cast initializer
    int q = (int) 5.0;
    printf("%d \n", q);

    // unary initializer
    int r = ++a;
    printf("%d \n", r);
    int s = --a;
    printf("%d \n", s);
    int t = -a;
    printf("%d \n", t);
    int u = ~a;
    printf("%d \n", u);
    int v = !a;
    printf("%d \n", v);
    int w = sizeof(a);
    printf("%d \n", w);

    // postfix initializer
    int x = a ++;
    printf("%d \n", x);
    int y = a --;
    printf("%d \n", y);
    int z = (int){5};
    printf("%d \n", z);

    int aa, ab = 5;
}