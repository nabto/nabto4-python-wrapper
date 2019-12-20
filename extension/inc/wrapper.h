#ifndef NABTO_WRAPPER_H
#define NABTO_WRAPPER_H

#include <string>
#include "nabto_client_api.h"

int nabto_startup(std::string home_dir);
int nabto_shutdown(void);

struct Error {
    int status;
    std::string extra;
};

class SessionWrapper
{
private:
    nabto_handle_t m_session;

    SessionWrapper(const SessionWrapper&);
    SessionWrapper& operator=(SessionWrapper&);
public:
    SessionWrapper();
    ~SessionWrapper();

    int open_session(std::string id, std::string password);
    int close_session(void);
    Error rpc_set_default_interface(std::string interfaceDefinition);
    Error rpc_invoke(std::string url);
};

#endif