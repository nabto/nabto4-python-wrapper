#include <iostream>
#include "wrapper.h"



int nabto_startup(std::string home_dir) {
    return nabtoStartup(home_dir.c_str());
}

int nabto_shutdown(void) {
    return nabtoShutdown();
}

//----Profile Management API----

int nabto_create_profile(std::string email, std::string password) {
    return nabtoCreateProfile(email.c_str(), password.c_str());
}

int nabto_create_self_signed_profile(std::string id, std::string password) {
    return nabtoCreateSelfSignedProfile(id.c_str(), password.c_str());
}

int nabto_remove_profile(std::string id) {
    return nabtoRemoveProfile(id.c_str());
}

error nabto_get_fingerprint(std::string id) {
    error result;
    char fingerprint[16];
    result.status = nabtoGetFingerprint(id.c_str(), fingerprint);

    char fp[33] = {'\0'};
    const char* table = "0123456789abcdef";
    for(int i = 0; i < 16; i++) {
        fp[2 * i] = table[(static_cast<unsigned char>(fingerprint[i]) >> 4)];
        fp[2 * i + 1] = table[static_cast<unsigned char>(fingerprint[i] & 0x0f)];
    }
    result.extra = std::string(fp);
    return result;
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

error SessionWrapper::rpc_set_default_interface(std::string xml) {
    char* err;
    error result;
    result.status = nabtoRpcSetDefaultInterface(m_session, xml.c_str(), &err);
    if (result.status == NABTO_FAILED_WITH_JSON_MESSAGE) {
        result.extra = std::string(err);
        nabtoFree(err);
    }
    return result;
}

error SessionWrapper::rpc_invoke(std::string url) {
    char* response;
    error result;
    result.status = nabtoRpcInvoke(m_session, url.c_str(), &response);
    result.extra = std::string(response);
    nabtoFree(response);
    return result;
}

//----Query----
const char* nabto_status_str(int status) {
    return nabtoStatusStr(nabto_status_t(status));
}