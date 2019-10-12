struct TestStruct{
    int value       :8;
    double value2   :32;
} instance5, instance6;

enum TestEnum {val1, val2 = 0};

union Data {
    int value;
    double value2;
};

int main(){
    int a,b;
    struct TestStruct instance, instance7;
    struct TestStruct* instance2 = &instance;
    struct TestStruct instane7 = {.value .value2 = 5};

    enum TestEnum instance3(a, b);

    union Data instance4;

    customfloat f = 5.0;
    __typeof__(f) g;

    instance.value = 5;
    instance2->value2 = 5.3;

    printf("%d\n", (int)sizeof(instance));
    printf("%d\n", (int)sizeof(int));
    printf("%d\n", (int) _Alignof(struct TestClass));

    return 0;
}