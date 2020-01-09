import os, time, json
import urllib.parse
from nabto_client import nabto

PARENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
NABTO_HOME_DIRECTORY = os.path.join(PARENT_DIRECTORY, 'share', 'nabto')
NABTO_QUERIES = os.path.join(PARENT_DIRECTORY, 'unabto_queries.xml')

class NabtoDevice:
    deviceID: str 
    session: nabto.Session = None

    def __init__(self, id: str, session: nabto.Session):
        self.deviceID = id
        self.session = session

    def rpcInvoke(self, f: str, args: dict):
        if args:
            params = urllib.parse.urlencode(args)
            return self.session.rpcInvoke(f"nabto://{self.deviceID}/{f}?{params}")

        return self.session.rpcInvoke(f"nabto://{self.deviceID}/{f}")

    def addUser(self, user, fingerprint):
        resp = self.rpcInvoke("add_user.json", {"name": user, "fingerprint": fingerprint})
        return json.loads(resp)["response"]

    def getUsers(self) -> list:
        resp = self.rpcInvoke("get_users.json", {"start": 0, "count": 10})
        return json.loads(resp)["response"]["users"]

    def pairWithDevice(self, name: str):
        resp = self.rpcInvoke("pair_with_device.json", {"name": name})
        return json.loads(resp)["response"]

USER = "alex"
PASSWORD = "mypassword"

LOCAL_PORT = 18090
NABTO_HOST = "jkkecnxk.rxxbkt.trial.nabto.net"
REMOTE_HOST = "localhost"
REMOTE_PORT = 8090


def main():
    nabto.nabtoStartup(NABTO_HOME_DIRECTORY)
    print(nabto.nabtoVersionString())
    session = nabto.Session()
    session.open(USER, PASSWORD)
    with open(NABTO_QUERIES) as file:
        session.rpcSetDefaultInterface(file.read())
        dev = NabtoDevice(NABTO_HOST, session)
        print(dev.getUsers())
    
    tunnel = nabto.Tunnel()
    port = tunnel.openTcp(session, LOCAL_PORT, NABTO_HOST, REMOTE_HOST, REMOTE_PORT)
    print(f"Opened tunnel on port {port}")
    time.sleep(30)
    tunnel.close()
    session.close()
    nabto.nabtoShutdown()


if __name__ == "__main__":
    main()