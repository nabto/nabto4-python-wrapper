#include "wrapper.h"

void hello(void) {
    printf("Hello from C++\n");
}

void print_string(std::string str) {
    printf(str.c_str());
}


int nabto_startup(std::string home_dir) {
    return nabtoStartup(home_dir.c_str());
}

int nabto_shutdown(void) {
    return nabtoShutdown();
}