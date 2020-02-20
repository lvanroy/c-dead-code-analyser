bool test_constant_conditions(){
    int i = 0;
    while(10 < 5){
        i = 5;
    }
    if(i == 5){
        return false;
    }
    return true;
}

bool test_constant_conditions_2(){
    int i = 0;
    while(5 < 10){
        i = 5;
    }
    if(i == 5){
        return true;
    }
    return false;
}