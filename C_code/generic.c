#include <stdio.h>
int main(void)
{
    // _Generic keyword acts as a switch that chooses
    // operation based on data type of argument.
    printf("%d\n", _Generic( 1.0L, float:1, double:2,
                            long double:3, default:0));
    printf("%d\n", _Generic( 1L, float:1, double:2,
                            long double:3, default:0));
    printf("%d\n", _Generic( 1.0L, float:1, double:2,
                                      long double:3));
    return 0;
}