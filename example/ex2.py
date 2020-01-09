import os, time
from nabto_client import nabto

PARENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
NABTO_HOME_DIRECTORY = os.path.join(PARENT_DIRECTORY, 'share', 'nabto')

nabto.nabtoStartup(NABTO_HOME_DIRECTORY)
print(nabto.nabtoVersionString())
s = nabto.Session()
s.open("alex", "mypassword")
time.sleep(5)
s.close()
nabto.nabtoShutdown()