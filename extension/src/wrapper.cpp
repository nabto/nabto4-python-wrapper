#include <iostream>
#include "wrapper.h"



int nabto_startup(std::string home_dir) {
    return nabtoStartup(home_dir.c_str());
}

int nabto_shutdown(void) {
    return nabtoShutdown();
}

SessionWrapper::SessionWrapper(): m_session(nullptr) {
     std::cout << "SessionWrapper::ctor" << std::endl;
}

SessionWrapper::~SessionWrapper() {
    std::cout << "SessionWrapper::dtor" << std::endl;
    if (m_session != nullptr) {
        nabto_status_t status = nabtoCloseSession(m_session);
        if (status != NABTO_OK) {
            std::cerr << "Could not close nabto session: "<< status << '\n';
        }
    }
}

int SessionWrapper::open_session(std::string id, std::string password) {
    return nabtoOpenSession(&m_session, id.c_str(), password.c_str());
}

int SessionWrapper::close_session(void) {
    nabto_handle_t session = m_session;
    m_session = nullptr;
    return nabtoCloseSession(session);
}

Error SessionWrapper::rpc_set_default_interface(std::string xml) {
    char* err;
    Error result;
    result.status = nabtoRpcSetDefaultInterface(m_session, xml.c_str(), &err);
    if (result.status == NABTO_FAILED_WITH_JSON_MESSAGE) {
        result.extra = std::string(err);
        nabtoFree(err);
    }
    return result;
}

Error SessionWrapper::rpc_invoke(std::string url) {
    char* response;
    Error result;
    result.status = nabtoRpcInvoke(m_session, url.c_str(), &response);
    result.extra = std::string(response);
    nabtoFree(response);
    return result;
}