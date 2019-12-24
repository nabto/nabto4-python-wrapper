from time import sleep
from memory_profiler import profile

import nabto_client


@profile
def nabto_stuff():
    nabto_client.startup("/home/alex/work/nabto/python-nabto-client/example/share/nabto")
    nabto_client.NabtoProfile.createSelfSignedProfile("alex", "mypassword")

    with nabto_client.NabtoSession("alex6", "mypassword6") as session, \
            nabto_client.NabtoTunnel(session, 0, 'sdktnens.ru4bi.appmyproduct.com', 'localhost', 6001) as port:
        print(f'Opened tunnel on port {port}')
        sleep(3)
    nabto_client.shutdown()

nabto_stuff()
