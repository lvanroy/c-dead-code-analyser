int main(){
    // primary initializer
    char a = 'a';

    // assignment initializer
    char b = a = 'q';

    // conditional initializer
    char c = a == 5 ? 110 : 101;

    // logical or initializer
    char d = 99 || 140;

    // logical and initializer
    char e = 200 && 100;

    // inclusive or initializer
    char f = 126 | 0;

    // exclusive or initializer
    char g = 109 ^ 0;

    // and initializer
    char h = 99 ^ 0 && 93;

    // equality initializer
    char i = 103 == 140;

    // relational initializer
    char j = 106 < 99;

    // shift initializer
    char k = 30 << 2;

    // additive initializer
    char l = a + 5;
    char m = a - 5;

    // multiplicative initializer
    char n = (char)(b * 1);
    char o = (char)(f / 2);
    char p = 8 % 3;

    // cast initializer
    char q = (char) 92;

    // unary initializer
    char r = ++a;
    char s = --a;
    char t = -(-a);
    char v = !a;
    char w = sizeof(a);

    // postfix initializer
    char x = a ++;
    char y = a --;
    char z = (char){109};
}