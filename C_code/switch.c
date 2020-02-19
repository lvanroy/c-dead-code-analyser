bool test_switch(){
    int a = 0;
    if(a == 0){
        switch(a) {
            case 5:
                a ++;
                a ++;
                return true;
                break;
                a++;
            case 3:
                a++;
            default:
                a++;
        }

        a ++;
        return true;
    }
    else{
        a += 5;
        return true;
    }

    return true;
}