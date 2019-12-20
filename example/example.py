import nabto_client
import nabto_client.nabto_api as nabto_api
from memory_profiler import profile

nabto_client.say_hello()
nabto_api.hello()
nabto_api.print_string("Hello from Python and C++")

@profile
def nabto_stuff():
    ok = nabto_api.nabto_startup("/home/alex/work/nabto/python-nabto-client/example")
    if ok == nabto_api.Status.NABTO_OK:
        print("Successful startup")
    else:
        print("Startup failed")

    session = None
    ok = nabto_api.nabtoOpenSession(session, "cloud", "password")
    if ok == nabto_api.NABTO_OK:
        print("Session opened")
    else:
        print("Error opening session:", ok)
    
nabto_stuff()
