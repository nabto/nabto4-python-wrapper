import nabto_client.nabto_api as api
from nabto_client.exception import NabtoException

class NabtoSession:
    session = None

    def __init__(self):
        self.session = api.SessionWrapper()

    def openSession(self, user, password):
        status = self.session.open_session(user, password)
        if status != api.Status.NABTO_OK:
            raise NabtoException(status)

    def closeSession(self):
        if self.session.close_session() != api.Status.NABTO_OK:
            raise Exception("NabtoError")

    def RpcSetDefaultInterface(self, interface):
        err = self.session.rpc_set_default_interface(interface)
        if err.status == api.Status.NABTO_FAILED_WITH_JSON_MESSAGE:
            raise Exception(err.extra)
        if err.status != api.Status.NABTO_OK:
            raise Exception("NabtoError: " + err.status)
        
    def RpcInvoke(self, url):
        err = self.session.rpc_invoke(url)
        if err.status == api.Status.NABTO_FAILED_WITH_JSON_MESSAGE:
            raise Exception(err.extra)
        if err.status != api.Status.NABTO_OK:
            raise Exception("NabtoError: " + err.status)
        return err.extra