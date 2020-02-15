#include "stdio.h"

int main(){
    // primary initializer
    char a = 'a';
    printf("%d \n", a);

    // assignment initializer
    char b = a = 'q';
    printf("%d \n", b);

    // conditional initializer
    char c = a == 5 ? 110 : 101;
    printf("%d \n", c);

    // logical or initializer
    char d = 99 || 140;
    printf("%d \n", d);

    // logical and initializer
    char e = 200 && 100;
    printf("%d \n", e);

    // inclusive or initializer
    char f = 126 | 0;
    printf("%d \n", f);

    // exclusive or initializer
    char g = 109 ^ 0;
    printf("%d \n", g);

    // and initializer
    char h = 99 ^ 0 && 93;
    printf("%d \n", h);

    // equality initializer
    char i = 103 == 140;
    printf("%d \n", i);

    // relational initializer
    char j = 106 < 99;
    printf("%d \n", j);

    // shift initializer
    char k = 30 << 2;
    printf("%d \n", k);

    // additive initializer
    char l = a + 5;
    printf("%d \n", l);
    char m = a - 5;
    printf("%d \n", m);

    // multiplicative initializer
    char n = (char)(b * 1);
    printf("%d \n", n);
    char o = (char)(f / 2);
    printf("%d \n", o);
    char p = 8 % 3;
    printf("%d \n", p);

    // cast initializer
    char q = (char) 72;
    printf("%d \n", q);

    // unary initializer
    char r = ++a;
    printf("%d \n", r);
    char s = --a;
    printf("%d \n", s);
    char t = -(-a);
    printf("%d \n", t);
    char v = !a;
    printf("%d \n", v);
    char w = sizeof(a);
    printf("%d \n", w);

    // postfix initializer
    char x = a ++;
    printf("%d \n", x);
    char y = a --;
    printf("%d \n", y);
    char z = (char){109};
    printf("%d \n", z);
}