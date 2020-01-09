import nabto_client.nabto as nabto


def startup(home_dir: str):
    return nabto.nabtoStartup(home_dir)


def shutdown():
    return nabto.nabtoShutdown()

def versionString():
    return nabto.nabtoVersionString()


class NabtoSession:
    def __init__(self, user: str, password: str):
        self.user = user
        self.password = password
        self.session = nabto.Session()

    def __enter__(self):
        self.open()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        self.session = None

    def open(self):
        return self.session.open(self.user, self.password)

    def close(self):
        return self.session.close()

    def RpcSetDefaultInterface(self, interface: str):
        return self.session.rpcSetDefaultInterface(interface)

    def RpcInvoke(self, url: str):
        return self.session.rpcInvoke(url)
