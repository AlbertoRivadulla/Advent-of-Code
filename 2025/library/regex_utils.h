#ifndef REGEX_UTILS_H
#define REGEX_UTILS_H

#include <regex.h>
#include <string.h>

void extract_group(const char *source, regmatch_t match, char *dest, size_t dest_size);

#endif
