#include "stdio.h"

int main(){
    int a = 5;
    int b = 2;

    // base assignment operation
    a = 2;
    printf("%d \n", a);

    // to test the revert cast to multiplication function
    a = (a) * 2;
    printf("%d \n", a);
    a = (a) + 2;
    printf("%d \n", a);
    a = (a) - 2;
    printf("%d \n", a);
    a = (a * b) * 2;
    printf("%d \n", a);
    a = (a * b) + 2;
    printf("%d \n", a);
    a = (a * b * b) * 2;
    printf("%d \n", a);

    // assignments using special assignment operator
    a *= 8;
    printf("%d \n", a);
    a /= 4;
    printf("%d \n", a);
    a %= 3;
    printf("%d \n", a);
    a += 3;
    printf("%d \n", a);
    a -= 2;
    printf("%d \n", a);
    a <<= 2;
    printf("%d \n", a);
    a >>= 1;
    printf("%d \n", a);
    a &= 4;
    printf("%d \n", a);
    a |= 13;
    printf("%d \n", a);
    a ^= 4;
    printf("%d \n", a);

    // assignment using assignment expression
    a = b = 20;
    printf("%d \n", a);
    printf("%d \n", b);

    // conditional assignment
    a = a == 20 ? 3 : 4;
    printf("%d \n", a);

    // logical or assignment
    a = 5 || 0;
    printf("%d \n", a);

    // logical and assignment
    a = 2 && 3;
    printf("%d \n", a);

    // inclusive or assignment
    a = 2 | 0;
    printf("%d \n", a);

    // exclusive or assignment
    a = 2 ^ 0;
    printf("%d \n", a);

    // and assignment
    a = 2 ^ 0 && 5;
    printf("%d \n", a);

    // equality assignment
    a = 2 == 3;
    printf("%d \n", a);

    // relational assignment
    a = 2 < 3;
    printf("%d \n", a);

    // shift assignment
    a = 2 << 2;
    printf("%d \n", a);

    // additive assignment
    a = a + 5;
    printf("%d \n", a);
    a = a - b;
    printf("%d \n", a);

    // multiplicative assignment
    a = b * 2;
    printf("%d \n", a);
    a = b / 5;
    printf("%d \n", a);
    a = a % 3;
    printf("%d \n", a);

    // cast assignment
    a = (int) 5.0;
    printf("%d \n", a);

    // unary assignment
    a = ++a;
    printf("%d \n", a);
    a = --a;
    printf("%d \n", a);
    a = -a;
    printf("%d \n", a);
    a = ~a;
    printf("%d \n", a);
    a = !a;
    printf("%d \n", a);
    a = sizeof(a);
    printf("%d \n", a);

    // postfix assignment
    a = a ++;
    printf("%d \n", a);
    a = a --;
    printf("%d \n", a);
    a = (int){5};
    printf("%d \n", a);
}