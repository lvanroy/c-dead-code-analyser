#include "stdio.h"

int main(){
    // primary initializer
    float a = 0;
    printf("%f \n", a);

    // assignment initializer
    float b = a = 5.2;
    printf("%f \n", b);

    // conditional initializer
    float c = a == 5 ? 3.1 : 4.5;
    printf("%f \n", c);

    // logical or initializer
    float d = 5.4 || 3.6;
    printf("%f \n", d);

    // logical and initializer
    float e = 2.2 && 3.6;
    printf("%f \n", e);

    // inclusive or initializer
    float f = 2 | 0;
    printf("%f \n", f);

    // exclusive or initializer
    float g = 2 ^ 0;
    printf("%f \n", g);

    // and initializer
    float h = 2 ^ 0 && 5.3;
    printf("%f \n", h);

    // equality initializer
    float i = 2.1 == 3.0;
    printf("%f \n", i);

    // relational initializer
    float j = 2.9 < 3.4;
    printf("%f \n", j);

    // shift initializer
    float k = 2 << 2;
    printf("%f \n", k);

    // additive initializer
    float l = a + 5.7;
    printf("%f \n", l);
    float m = a - b;
    printf("%f \n", m);

    // multiplicative initializer
    float n = b * 2.0;
    printf("%f \n", n);
    float o = b / 5.4;
    printf("%f \n", o);
    float p = 8 % 3;
    printf("%f \n", p);

    // cast initializer
    float q = (float) 5;
    printf("%f \n", q);

    // unary initializer
    float r = ++a;
    printf("%f \n", r);
    float s = --a;
    printf("%f \n", s);
    float t = -a;
    printf("%f \n", t);
    float u = ~5;
    printf("%f \n", u);
    float v = !a;
    printf("%f \n", v);
    float w = sizeof(a);
    printf("%f \n", w);

    // postfix initializer
    float x = a ++;
    printf("%f \n", x);
    float y = a --;
    printf("%f \n", y);
    float z = (float){5.1};
    printf("%f \n", z);
}