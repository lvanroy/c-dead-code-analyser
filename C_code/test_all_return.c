bool if_all_return(int a){
    if(a == 5){
        a++;
        return true;
    }
    else{
        a--;
        return true;
    }
    a = 10;
    return false;
}

bool switch_all_return(int a){
    switch(a)
        default:
            return true;

    a ++;
    return false;
}

bool switch_all_return_2(int a){
    switch(a){
        case 5:
            return true;
        case 10:
            return true;
        default:
            return true;
    }

    a ++;
    return false;
}