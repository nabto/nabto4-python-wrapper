import nabto_client.nabto_api as api
from nabto_client.exception import check_status, check_result


class NabtoSession:
    def __init__(self, user, password):
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
    def RpcSetDefaultInterface(self, interface):
        return self.session.rpc_set_default_interface(interface)
        
    @check_result
    def RpcInvoke(self, url):
        return self.session.rpc_invoke(url)
