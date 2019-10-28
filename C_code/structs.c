#include "stdio.h"

struct TestStruct{
    int value1       :8;
    int value2      :32;
} instance5, instance6;

enum TestEnum {val1, val2 = 0};

union Data {
    int value1;
    float value2;
};

int main(){
    int a,b;
    struct TestStruct instance, instance7;
    struct TestStruct* instance2 = &instance;
    struct TestStruct instance8 = {.value1 = 3, .value2 = 5};

    printf("%d\n", instance8.value1);

    enum TestEnum instance3 = val1;
    printf("%d\n", instance3);

    union Data instance4;

    __typeof__(a) g;

    instance.value1 = 5;
    instance2->value2 = 5.3;

    printf("%d\n", (int)sizeof(instance));
    printf("%d\n", (int)sizeof(int));
    printf("%d\n", (int) _Alignof(struct TestStruct));

    return 0;
}