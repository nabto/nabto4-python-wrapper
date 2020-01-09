import json
import os
import urllib.parse
from time import sleep

import nabto_client


class NabtoDevice:
    deviceID: str 
    session: nabto_client.NabtoSession = None

    def __init__(self, id: str, session: nabto_client.NabtoSession):
        self.deviceID = id
        self.session = session

    def rpcInvoke(self, f: str, args: dict):
        if args:
            params = urllib.parse.urlencode(args)
            return self.session.RpcInvoke(f"nabto://{self.deviceID}/{f}?{params}")

        return self.session.RpcInvoke(f"nabto://{self.deviceID}/{f}")

    def addUser(self, user, fingerprint):
        resp = self.rpcInvoke("add_user.json", {"name": user, "fingerprint": fingerprint})
        return json.loads(resp)["response"]

    def getUsers(self) -> list:
        resp = self.rpcInvoke("get_users.json", {"start": 0, "count": 10})
        return json.loads(resp)["response"]["users"]

    def pairWithDevice(self, name: str):
        resp = self.rpcInvoke("pair_with_device.json", {"name": name})
        return json.loads(resp)["response"]


# /home/../python-nabto-client/example/share/nabto
PARENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
NABTO_HOME_DIRECTORY = os.path.join(PARENT_DIRECTORY, 'share', 'nabto')
NABTO_QUERIES = os.path.join(PARENT_DIRECTORY, 'unabto_queries.xml')

USER = "alex"
PASSWORD = "mypassword"

LOCAL_PORT = 7000
NABTO_HOST = "jkkecnxk.rxxbkt.trial.nabto.net"
REMOTE_HOST = "localhost"
REMOTE_PORT = 8090


def nabto_stuff():
    nabto_client.startup(NABTO_HOME_DIRECTORY)
    # nabto_client.NabtoProfile.createSelfSignedProfile(USER, PASSWORD)
    print(nabto_client.NabtoProfile.getFingerprint("alex"))

    with nabto_client.NabtoSession(USER, PASSWORD) as session:
        with open(NABTO_QUERIES) as file:
            session.RpcSetDefaultInterface(file.read())
            dev = NabtoDevice(NABTO_HOST, session)
            dev.addUser("cristi", "34e0834b008f0ee3748de75ecee71802")
            # print(dev.pairWithDevice(USER))
            print(dev.getUsers())
            return

        with nabto_client.NabtoTunnel(session, LOCAL_PORT, NABTO_HOST, REMOTE_HOST, 8090) as port:
            print(f'Opened tunnel on port {port}')
            sleep(30)
    nabto_client.shutdown()


nabto_stuff()
