#include "timer.h"
#include <stdio.h>

void timer_start(Timer *timer, const char *label) {
    timer->label = label;
    gettimeofday(&timer->start, NULL);
}

void timer_stop(Timer* timer) {
    gettimeofday(&timer->stop, NULL);

    double elapsed = (timer->stop.tv_sec - timer->start.tv_sec) +
                          (timer->stop.tv_usec - timer->start.tv_usec) / 1.E6;

    if (elapsed < 0.001) {
        printf("\n[TIMER] %s: %.2f us\n\n", timer->label, elapsed * 1.E6);
    } else if (elapsed < 1.0) {
        printf("\n[TIMER] %s: %.2f ms\n\n", timer->label, elapsed * 1.E3);
    } else {
        printf("\n[TIMER] %s: %.3f s\n\n", timer->label, elapsed);
    }
}

void time_function(const char *label, TimedFunction func) {
    Timer timer;
    timer_start(&timer, label);
    func();
    timer_stop(&timer);
}

