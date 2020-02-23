#include "stdio.h"
#include <stdbool.h>

int test(){
    bool a = true;
    bool b = false;
    bool arr[2] = {true, false};

    bool c = a && b;
    printf("c:0=%d\n", c);
    bool d = a || b;
    printf("d:1=%d\n", d);
    bool m = !d;
    printf("l:0=%d\n", m);

    bool f = 10 == 10;
    printf("f:1=%d\n", f);
    bool g = 10 != 11;
    printf("g:1=%d\n", g);
    bool h = 10 > 11;
    printf("h:0=%d\n",h);
    bool i = 10 >= 11;
    printf("i:0=%d\n", i);
    bool j = 10 < 11;
    printf("j:1=%d\n", j);
    bool k = 10 <= 11;
    printf("k:1=%d\n", k);

    bool l = 2 ^ 2;
    printf("l:0=%d\n", l);
    bool e = 2 & 4;
    printf("e:0=%d\n", e);
    bool n = 2 | 4;
    printf("n:1=%d\n", n);
}