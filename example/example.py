from time import sleep
from memory_profiler import profile

import nabto_client


@profile
def nabto_stuff():
    nabto_client.startup("/home/alex/work/nabto/python-nabto-client/example/share/nabto")
    # nabto_client.NabtoProfile.createSelfSignedProfile("alex", "mypassword")

    with nabto_client.NabtoSession("alex", "mypassword") as session:
        with open("./unabto_queries.xml") as file:
            session.RpcSetDefaultInterface(file.read())
            session.RpcInvoke("nabto://jkkecnxk.rxxbkt.trial.nabto.net/pair_with_device.json?name=alex")
        with nabto_client.NabtoTunnel(session, 0, 'jkkecnxk.rxxbkt.trial.nabto.net', 'localhost', 8090) as port:
            print(f'Opened tunnel on port {port}')
            sleep(30)
    nabto_client.shutdown()

nabto_stuff()
