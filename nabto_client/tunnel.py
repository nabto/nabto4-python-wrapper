from nabto_client import nabto_api as api
from nabto_client.exception import check_status, check_result
from nabto_client.session import NabtoSession


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
