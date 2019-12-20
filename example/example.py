import nabto_client
import nabto_client.nabto_api as nabto_api
from memory_profiler import profile

@profile
def nabto_stuff():
    ok = nabto_api.nabto_startup("/home/alex/work/nabto/python-nabto-client/example")
    if ok == nabto_api.Status.NABTO_OK:
        print("Successful startup")
    else:
        print("Startup failed")

    session = nabto_api.SessionWrapper()
    ok = session.open_session("cloud", "password")
    if ok == nabto_api.Status.NABTO_OK:
        print("Session opened")
    else:
        print("Error opening session:", ok)
    
nabto_stuff()
