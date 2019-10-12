struct TestClass{
int value;
double value2;
};

int main(){
    struct TestClass instance;
    struct TestClass* instance2 = &instance;

    instance.value = 5;
    instance2->value2 = 5.3;

    printf("%d\n", (int)sizeof(instance));
    printf("%d\n", (int) _Alignof(struct TestClass));

    return 0;
}