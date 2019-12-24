from nabto_client import nabto_api as api
from nabto_client.exception import check_status, check_result


@check_status
def startup(home_dir: str):
    return api.nabto_startup(home_dir)


@check_status
def shutdown():
    return api.nabto_shutdown()


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
