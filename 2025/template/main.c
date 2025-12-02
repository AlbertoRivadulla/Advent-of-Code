#include <stdio.h>
#include <stdlib.h>

#include <time.h>

#include "utils.h"
#include "timer.h"

void first_part() {
    // TODO:
    return;
}

void second_part() {
    // TODO:
    return;
}

int main() {
    Timer timer;

    timer_start(&timer, "First part");
    first_part();
    timer_stop(&timer);

    timer_start(&timer, "Second part");
    second_part();
    timer_stop(&timer);


    return 0;
}
