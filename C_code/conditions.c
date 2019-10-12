bool main(){
    int x = 0;
    int y = 0;
    for((x(0)); x < 10; x ++){
        y ++;
    }
    for(x=5, x=3;x<20; ++x){
        --y;
    }

    LOOP: for(void x();x<5; x++){
        goto Loop;
    }

    if(x > 20 && x >= 10 || y <= 25){
        return false;
    }

    if(x == 5 && y != 10){
        return true;
    }

    if(x & 5 && y | 4 && y ^ 5){
        return true;
    }

    int a = true ? x : y;

    a *= 5;

    _Static_assert(0, "lalala");

    do {a++;} while (a < 300);

    return true;
}