bool test_invalid_expression(int a){
    int counter = 5;
    int counter2 = a;

    if(counter < 5){
        return true;
    }

    counter *= 5;
    counter /= 5;
    counter %= 5;
    counter <<= 5;
    counter >>= 5;
    counter &= 5;
    counter ^= 5;
    counter |= 5;

    counter = counter << 2;
    counter = counter >> 2;

    counter += counter2;
    counter -= counter2;

    counter += counter;
    counter -= counter;
    counter += a;
    counter -= a;
    counter += 5;
    counter -= 5;

    counter = counter + counter2;
    counter = counter - counter2;

    counter *= a;
    counter /= a;
    counter %= a;
    counter <<= a;
    counter >>= a;
    counter &= a;
    counter ^= a;
    counter |= a;

    counter = counter * counter2;
    counter = counter / counter2;
    counter = counter % counter2;

    counter = -a;
    counter = +a;

    counter = counter << a;
    counter = counter >> a;

    return false;
}