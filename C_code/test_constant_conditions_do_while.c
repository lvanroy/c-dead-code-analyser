bool test_constant_conditions(){
    int i = 0;
    do{
        i=5;
    }
    while(10 < 5);

    if(i == 5){
        return false;
    }
    return true;
}

bool test_constant_conditions_2(){
    int i = 0;
    do{
        i=5;
    }
    while(5 < 10);

    if(i == 5){
        return true;
    }
    return false;
}