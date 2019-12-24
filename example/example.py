import nabto_client
import nabto_client.nabto_api as nabto_api
from memory_profiler import profile

@profile
def nabto_stuff():
    ok = nabto_api.nabto_startup("/home/alex/work/nabto/python-nabto-client/example/share/nabto")
    if ok == nabto_api.Status.NABTO_OK:
        print("Successful startup")
    else:
        print("Startup failed")

    nabto_api.nabto_create_self_signed_profile("alex", "mypassword")

    with nabto_client.NabtoSession("alex", "mypassword") as session, \
            nabto_client.NabtoTunnel(session, 0, 'sdktnens.ru4bi.appmyproduct.com', 'localhost', 6001) as port:
        print(f'Opened tunnel on port {port}')

nabto_stuff()
