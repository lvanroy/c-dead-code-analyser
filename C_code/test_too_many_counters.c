int test_too_many_counters(int a, int b){
    int counter1 = a;
    int counter2 = a;

    if(counter1 < counter2){
        return false;
    }

    if(a < b){
        return true;
    }
}