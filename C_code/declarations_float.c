int main(){
    // primary initializer
    float a = 0;

    // assignment initializer
    float b = a = 5.2;

    // conditional initializer
    float c = a == 5 ? 3.1 : 4.5;

    // logical or initializer
    float d = 5.4 || 3.6;

    // logical and initializer
    float e = 2.2 && 3.6;

    // inclusive or initializer
    float f = 2 | 0;

    // exclusive or initializer
    float g = 2 ^ 0;

    // and initializer
    float h = 2 ^ 0 && 5.3;

    // equality initializer
    float i = 2.1 == 3.0;

    // relational initializer
    float j = 2.9 < 3.4;

    // shift initializer
    float k = 2 << 2;

    // additive initializer
    float l = a + 5.7;
    float m = a - b;

    // multiplicative initializer
    float n = b * 2.0;
    float o = b / 5.4;
    float p = 8 % 3;

    // cast initializer
    float q = (float) 5;

    // unary initializer
    float r = ++a;
    float s = --a;
    float t = -a;
    float u = ~5;
    float v = !a;
    float w = sizeof(a);

    // postfix initializer
    float x = a ++;
    float y = a --;
    float z = (float){5.1};
}