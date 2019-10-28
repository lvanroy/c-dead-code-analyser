#include "stdio.h"

struct Books {
    char* title;
    char* author;
    char subject[100];
    int book_id;
} book;

union numberRepresentation{
    int option1;
    float option2;
};

enum week{Mon, Tue, Wed, Thur, Fri, Sat, Sun};

int main() {
    book.title = "Lord Of The Rings";
    book.author = "J.R.R. Tolkien";
    book.book_id = 2;
    printf("%d\n", book.title[0]);
    printf("%d\n", book.book_id);

    struct Books book2 = (struct Books) {.title="The Davinci Code", .author="Dan Brown",
            .subject="long story", .book_id=1};

    printf("%d\n", book2.title[0]);
    printf("%d\n", book2.book_id);

    struct Books* book3 = &book2;

    printf("%d\n", book3->title[0]);
    printf("%d\n", book3->book_id);

    union numberRepresentation integer = (union numberRepresentation) {.option1 = 5};

    printf("%d\n", integer.option1);

    union numberRepresentation reel;
    reel.option2 = 'c';

    printf("%f\n", reel.option2);

    enum week day;
    day = Wed;

    printf("%d\n", day);

    enum week day2 = (enum week) {Tue};

    printf("%d\n", day2);
}