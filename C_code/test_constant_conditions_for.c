bool test_constant_conditions(){
    int i = 0;
    for(int i = 0; 10 < 5; i++){
        i = 5;
    }
    if(i == 5){
        return false;
    }
    return true;
}

bool test_constant_conditions_2(){
    int i = 0;
    for(int i = 0; 5 < 10; i++){
        i = 5;
    }
    if(i == 5){
        return true;
    }
    return false;
}