#include <iostream>
#include <sstream>
#include <chrono>
#include <thread>
#include "wrapper.h"


//----Session API----

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
            std::cerr << "Could not close nabto session: "<< nabtoStatusStr(status) << '\n';
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

//----Tunnel API----

TunnelWrapper::TunnelWrapper(): m_tunnel(nullptr) {
    std::cout << "TunnelWrapper::ctor" << std::endl;
}

TunnelWrapper::~TunnelWrapper() {
    std::cout << "TunnelWrapper::dtor" << std::endl;
    if (m_tunnel != nullptr) {
        nabto_status_t status = nabtoTunnelClose(m_tunnel);
        if (status != NABTO_OK) {
            std::cerr << "Could not close nabto tunnel: "<< nabtoStatusStr(status) << '\n';
        }
    }
}

error TunnelWrapper::open_tcp(SessionWrapper& session, int localPort, std::string nabtoHost, std::string remoteHost, int remotePort) {
    error result;
    result.status = nabtoTunnelOpenTcp(
        &m_tunnel, 
        session.m_session, 
        localPort, 
        nabtoHost.c_str(),
        remoteHost.c_str(),
        remotePort
    );
    if (result.status != NABTO_OK) {
        return result;
    }
    nabto_tunnel_state_t tunnelState = NTCS_CLOSED;
    while (tunnelState < NTCS_LOCAL) {
        result.status = nabtoTunnelInfo(m_tunnel, NTI_STATUS, sizeof(tunnelState), &tunnelState);
        if (result.status != NABTO_OK) {
            return result;
        }
        if (tunnelState == NTCS_CLOSED) {
            return result;
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
    int port;
    result.status = nabtoTunnelInfo(m_tunnel, NTI_PORT, sizeof(port), &port);
    if (result.status != NABTO_OK) {
        return result;
    }
    std::stringstream ss;
    ss << port;
    ss >> result.extra;
    return result;    
}

int TunnelWrapper::close() {
    if (m_tunnel != nullptr) {
        nabto_status_t status = nabtoTunnelClose(m_tunnel);
        if (status == NABTO_OK) {
            m_tunnel = nullptr;
        }
        return status;
    }
    return NABTO_OK;
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

//----Query----
const char* nabto_status_str(int status) {
    return nabtoStatusStr(nabto_status_t(status));
}