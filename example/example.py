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
    session = nabto_client.NabtoSession()
    session.openSession("alex", "mypassword")
    
nabto_stuff()
