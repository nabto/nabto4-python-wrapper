import os
from nabto_client import nabto

PARENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
NABTO_HOME_DIRECTORY = os.path.join(PARENT_DIRECTORY, 'share', 'nabto')

nabto.nabtoStartup(NABTO_HOME_DIRECTORY)
print(nabto.nabtoVersionString())
nabto.nabtoShutdown()