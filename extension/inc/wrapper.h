#ifndef NABTO_WRAPPER_H
#define NABTO_WRAPPER_H

#include <string>
#include "nabto_client_api.h"

struct error {
    int status;
    std::string extra;
};

//----Session API----
int nabto_startup(std::string home_dir);
int nabto_shutdown(void);

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
    error rpc_set_default_interface(std::string interfaceDefinition);
    error rpc_invoke(std::string url);
};

//----Profile Management API----
int nabto_create_profile(std::string email, std::string password);
int nabto_create_self_signed_profile(std::string id, std::string password);
int nabto_remove_profile(std::string id);
error nabto_get_fingerprint(std::string id);

//----Query----
const char* nabto_status_str(int status);

#endif