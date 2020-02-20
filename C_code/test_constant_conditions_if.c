bool test_constant_conditions(){
    int i = 0;
    if(5 < 10){
        i ++;
    }
    else if(10 < 20){
        i ++;
    }
    if(i == 1){
        return true;
    }
    return false;
}

bool test_constant_conditions_2(){
    int i = 0;
    if(10 < 5){
        i ++;
    }
    else if(10 < 20){
        i ++;
    }
    if(i == 1){
        return true;
    }
    return false;

}