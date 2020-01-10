import nabto_client.nabto as nabto
from nabto_client.session import NabtoSession

class NabtoTunnel:
    def __init__(self, session: NabtoSession, localPort: int, nabtoHost: str, remoteHost: str, remotePort: int):
        self.session = session.session
        self.localPort = localPort
        self.nabtoHost = nabtoHost
        self.remoteHost = remoteHost
        self.remotePort = remotePort
        self.tunnel = nabto.Tunnel()

    def __enter__(self):
        return self.openTcp()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        self.tunnel = None

    def openTcp(self):
        return self.tunnel.openTcp(self.session, self.localPort, self.nabtoHost, self.remoteHost, self.remotePort)

    def close(self):
        return self.tunnel.close()

    def status(self):
        return self.tunnel.status()

class TunnelStatus:
    CLOSED              = -1
    CONNECTING          = 0
    READY_FOR_RECONNECT = 1
    UNKNOWN             = 2
    LOCAL               = 3
    REMOTE_P2P          = 4
    REMOTE_RELAY        = 5
    REMOTE_RELAY_MICRO  = 6 