long double test(){
    int x = 0;
    int y = 0;
    for(((func(5))); x < 10; x ++){
        y ++;
    }
    for(x=5, x=3;x<20, y>10; ++x){
        --y;
    }

    LOOP: for(void x();y<5; y++){
        goto LOOP;
    }

    for(; q < 10; q++){}

    if(x > 20 && x >= 10 || y <= 25){
        return false;
    }

    if(x == 5 && y != 10){
        continue;
        return true;
    }

    if(x & 5 && y | 4 && y ^ 5){
        return true;
    }

    while(x > 5, x++){
        break;
    }

    int a = true ? x : y;

    a *= 5;

    _Static_assert(0, "test");

    do {a++;} while (a < 300, b < 200);

    return true;
}