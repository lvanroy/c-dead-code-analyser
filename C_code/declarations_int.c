int main(){
    // integers
    int a = 0;

    // assignment initializer
    int g = a = 5;

    // conditional initializer
    int h = a == 5 ? 3 : 4;

    // logical or initializer
    int i = 5 || 0;

    // logical and initializer
    int j = 2 && 3;

    // inclusive or initializer
    int k = 2 | 0;

    // exclusive or initializer
    int l = 2 ^ 0;

    // and initializer
    int m = 2 ^ 0 && 5;

    // equalitiy initializer
    int n = 2 == 3;

    // basic additive initializer
    int b = a + 5;
    int c = a - b;

    // basic multiplicative initializer
    int d = b * 2;
    int e = b / 5;
    int f = d % 3;
}