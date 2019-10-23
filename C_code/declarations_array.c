#include "stdio.h"

int main(){
    // initialise using constant
    int a[5] = {1, 2, 3.2, 4, 5};
    printf("%i\n", a[1]);

    float b[5] = {1, 'c', 5.0, 5.5, 6.2};
    printf("%f\n", b[0]);
    printf("%f\n", b[1]);

    char c[5] = {'c', 'q', -5, 5.32, 4};
    printf("%d\n", c[1]);
    printf("%d\n", c[3]);

    char d[5] = "world";
    printf("%d\n", d[2]);

    char* e = "test";
    printf("%d\n", e[3]);

    // initialise without size
    int f[] = {1, 2, 3, 500, -90};
    printf("%i\n", f[4]);

    float g[] = {2, 'a', -50, 3, 9};
    printf("%f\n", g[2]);

    char h[] = {'A', '=', 5, 5.3, 99};
    printf("%i\n", h[1]);

    // initialise with string
    char i[] = "Hello";
    printf("%d\n", i[0]);
}