import nabto_client.nabto_api as api
from nabto_client.exception import check_status, check_result


class NabtoSession:
    session = None

    def __init__(self):
        self.session = api.SessionWrapper()

    @check_status
    def openSession(self, user, password):
        return self.session.open_session(user, password)

    @check_status
    def closeSession(self):
        return self.session.close_session()

    @check_result
    def RpcSetDefaultInterface(self, interface):
        return self.session.rpc_set_default_interface(interface)
        
    @check_result
    def RpcInvoke(self, url):
        return self.session.rpc_invoke(url)
