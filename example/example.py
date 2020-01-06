from time import sleep
import urllib.parse
import json
from memory_profiler import profile

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
    
    def getUsers(self) -> list:
        resp = self.rpcInvoke("get_users.json",{"start":0,"count": 10})
        return json.loads(resp)["response"]["users"]

    def pairWithDevice(self, name: str):
        resp = self.rpcInvoke("pair_with_device.json", {"name": name})
        return json.loads(resp)["response"]

@profile
def nabto_stuff():
    nabto_client.startup("/home/alex/work/nabto/python-nabto-client/example/share/nabto")
    # nabto_client.NabtoProfile.createSelfSignedProfile("alex", "mypassword")

    with nabto_client.NabtoSession("alex", "mypassword") as session:
        with open("./unabto_queries.xml") as file:
            session.RpcSetDefaultInterface(file.read())
            dev = NabtoDevice("jkkecnxk.rxxbkt.trial.nabto.net", session)
            print(dev.pairWithDevice("alex"))
        with nabto_client.NabtoTunnel(session, 0, 'jkkecnxk.rxxbkt.trial.nabto.net', 'localhost', 8090) as port:
            print(f'Opened tunnel on port {port}')
            sleep(30)
    nabto_client.shutdown()

nabto_stuff()
