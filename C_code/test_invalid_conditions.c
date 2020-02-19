bool test_invalid_conditions(int a){
    int counter = a;

    if(counter > 5){
        return true;
    }

    if(counter >= 5){
        return true;
    }

    if(counter == 5){
        return true;
    }

    if(counter != 5){
        return true;
    }

    if(counter < 5){
        return true;
    }

    if(counter <= 5){
        return true;
    }

    if(counter & 5){
        return false;
    }

    if(counter | 5){
        return false;
    }

    if(counter ^ 5){
        return false;
    }

    if(counter == 5 && counter != 5){
        return false;
    }

    if(counter == 5 || counter != 5){
        return false;
    }
}