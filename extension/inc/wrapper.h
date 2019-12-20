#ifndef NABTO_WRAPPER_H
#define NABTO_WRAPPER_H

#include <string>
#include "nabto_client_api.h"

void hello(void);
void print_string(std::string str);

int nabto_startup(std::string home_dir);
int nabto_shutdown(void);


#endif