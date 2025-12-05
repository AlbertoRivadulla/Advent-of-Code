#include "regex_utils.h"

#include <stdio.h>

void extract_group(const char *source, regmatch_t match, char *dest, size_t dest_size) {
    // Case in which the match is empty
    if (match.rm_so == -1) {
        dest[0] = '\0';
        return;
    }

    // match.rm_so -> start offset (first index of the match in the string)
    // match.rm_eo -> end offset
    size_t len = match.rm_eo - match.rm_so;
    if (len >= dest_size) {
        len = dest_size - 1;
    }

    strncpy(dest, source + match.rm_so, len);
    dest[len] = '\0';
}

