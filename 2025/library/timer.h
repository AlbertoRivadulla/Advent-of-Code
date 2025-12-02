#ifndef TIMER_H
#define TIMER_H

#include <sys/time.h>

typedef struct {
    struct timeval start;
    struct timeval stop;
    const char* label;
} Timer;

void timer_start(Timer* timer, const char* label);
void timer_stop(Timer* timer);

typedef void (*TimedFunction)(void);
void time_function(const char* label, TimedFunction func);

#endif
