 #include <stdbool.h>
#include <cstdio>

bool for_loops(int a){
    int i = 0;
    int k = 0;

    for(int j = 0,j = 5, j = 8, l = 5; j < 3; j ++){
        continue;
    }

    for(i = 2, i = 8;i != 5; k++, i++, i++){
        continue;
        i += 1;
        break;
    }

    i = a + i;

    for(i=5, k = 10;;){
        break;
    }

    for(i = a;;){
        break;
    }

    for(;i > 500;){return true;}

    for(;;i++, k++){
        if(i == 10){
            i = 9;
            break;
        }
        else{
            i = 10;
        }
    }

    return true;
}

bool while_loops(int b){
    int i = 0;

    while(i <= b){
        i ++;
    }

    while((i != b)){
        i--;
        break;
    }

    while(i == b){

        i --;
    }

    while(i > 0){i -= 1;i-=1;}

    return true;
}

bool do_while_loops(int c){
    int i = 10;

    do {
        i++;
    }
    while(i <= c);

    do {
        i--;
        break;
    }
    while(i == 0);

    do{
        i --;
    }
    while(i == c);

    do{i -= 1;}while(i>0);

    return true;
}

bool if_statements(int d){
    int i;

    if(i != 0){
        i = 6;
    }

    if(i == 5){
        i -= 5;
    }

    if(i > 3){
        i = d;
    }
    else if(i <= 4){
        return true;
    }
    else{
        i = 5;
    }

    return true;
}