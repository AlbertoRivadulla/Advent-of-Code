#include <stdio.h>
#include <stdlib.h>

#include <time.h>

#include "utils.h"
#include "timer.h"

void test_timer() {
    printf("eeeee\n");
}

// int main(int argc, char* argv[]) {
int main() {
    clock_t begin = clock();

    Timer timer;
    timer_start(&timer, "Test label");

    printf("Hello from main\n");


    int* numbers = malloc(5 * sizeof(int));
    if (numbers == NULL) {
        fprintf(stderr, "Memory allocation failure\n");
        return 1;
    }

    for (int i = 0; i < 5; ++i) {
        numbers[i] = i * 5;
        do_something(i);
        do_something(numbers[i]);
    }

    free(numbers);

    clock_t end = clock();

    printf("Execution time: %f s\n", (double)(end - begin) / CLOCKS_PER_SEC);

    timer_stop(&timer);

    time_function("timed function", test_timer);

    return 0;
}
