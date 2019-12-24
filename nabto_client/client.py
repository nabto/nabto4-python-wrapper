import nabto_client.nabto_api as api
from nabto_client.exception import check_status, check_result


class NabtoSession:
    def __init__(self, user: str, password: str):
        self.user = user
        self.password = password
        self.session = api.SessionWrapper()

    def __enter__(self):
        self.openSession()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closeSession()
        self.session = None

    @check_status
    def openSession(self):
        return self.session.open_session(self.user, self.password)

    @check_status
    def closeSession(self):
        return self.session.close_session()

    @check_result
    def RpcSetDefaultInterface(self, interface: str):
        return self.session.rpc_set_default_interface(interface)
        
    @check_result
    def RpcInvoke(self, url: str):
        return self.session.rpc_invoke(url)


class NabtoTunnel:
    def __init__(self, session: NabtoSession, localPort: int, nabtoHost: str, remoteHost: str, remotePort: int):
        self.session = session.session
        self.localPort = localPort
        self.nabtoHost = nabtoHost
        self.remoteHost = remoteHost
        self.remotePort = remotePort
        self.tunnel = api.TunnelWrapper()

    def __enter__(self):
        return self.openTcp()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        self.tunnel = None

    @check_result
    def openTcp(self):
        return self.tunnel.open_tcp(self.session, self.localPort, self.nabtoHost, self.remoteHost, self.remotePort)

    @check_status
    def close(self):
        return self.tunnel.close()


@check_status
def createProfile(email: str, password: str):
    return api.nabto_create_profile(email, password)


@check_status
def createSelfSignedProfile(id: str, password: str):
    return api.nabto_create_self_signed_profile(id, password)


@check_status
def removeProfile(id: str):
    return api.nabto_remove_profile(id)


@check_result
def getFingerprint(id: str):
    return api.nabto_get_fingerprint(id)
