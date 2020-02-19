#include "stdio.h"

union numberRepresentation{
    int option1;
    float option2;
};

int main(){
    union numberRepresentation a;
    int b = 6;

    // base assignment operation
    a.option1 = 7;
    printf("%d \n", a.option1);

    // assignments using special assignment operator
    a.option1 *= 8;
    printf("%d \n", a);
//    a.option1 /= 4;
//    printf("%d \n", a);
//    a.option1 %= 3;
//    printf("%d \n", a);
//    a.option1 += 3;
//    printf("%d \n", a);
//    a.option1 -= 2;
//    printf("%d \n", a);
//    a.option1 <<= 2;
//    printf("%d \n", a);
//    a.option1 >>= 1;
//    printf("%d \n", a);
//    a.option1 &= 4;
//    printf("%d \n", a);
//    a.option1 |= 13;
//    printf("%d \n", a);
//    a.option1 ^= 4;
//    printf("%d \n", a);
//
//    // assignment using assignment expression
//    a.option1 = b = 20;
//    printf("%d \n", a);
//    printf("%d \n", b);
//
//    // conditional assignment
//    a.option1 = a.option1 == 20 ? 3 : 4;
//    printf("%d \n", a);
//
//    // logical or assignment
//    a.option1 = 5 || 0;
//    printf("%d \n", a);
//
//    // logical and assignment
//    a.option1 = 2 && 3;
//    printf("%d \n", a);
//
//    // inclusive or assignment
//    a.option1 = 2 | 0;
//    printf("%d \n", a);
//
//    // exclusive or assignment
//    a.option1 = 2 ^ 0;
//    printf("%d \n", a);
//
//    // and assignment
//    a.option1 = 2 ^ 0 && 5;
//    printf("%d \n", a);
//
//    // equality assignment
//    a.option1 = 2 == 3;
//    printf("%d \n", a);
//
//    // relational assignment
//    a.option1 = 2 < 3;
//    printf("%d \n", a);
//
//    // shift assignment
//    a.option1 = 2 << 2;
//    printf("%d \n", a);
//
//    // additive assignment
//    a.option1 = a.option1 + 5;
//    printf("%d \n", a);
//    a.option1 = a.option1 - b;
//    printf("%d \n", a);
//
//    // multiplicative assignment
//    a.option1 = b * 2;
//    printf("%d \n", a);
//    a.option1 = b / 5;
//    printf("%d \n", a);
//    a.option1 = a.option1 % 3;
//    printf("%d \n", a);
//
//    // cast assignment
//    a.option1 = (int) 5.0;
//    printf("%d \n", a);
//
//    // unary assignment
//    a.option1 = ++a;
//    printf("%d \n", a);
//    a.option1 = --a;
//    printf("%d \n", a);
//    a.option1 = -a;
//    printf("%d \n", a);
//    a.option1 = ~a;
//    printf("%d \n", a);
//    a.option1 = !a;
//    printf("%d \n", a);
//    a.option1 = sizeof(a);
//    printf("%d \n", a);
//
//    // postfix assignment
//    a.option1 = a.option1 ++;
//    printf("%d \n", a);
//    a.option1 = a.option1 --;
//    printf("%d \n", a);
//    a.option1 = (int){5};
//    printf("%d \n", a);
}