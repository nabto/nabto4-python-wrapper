from nabto_client.nabto_api import nabto_status_str, Status

class NabtoException(Exception):
    def __init__(self, status, message=None):
        statusStr = nabto_status_str(status)
        if message:
            super().__init__("{}: {}".format(statusStr, message))
        else:
            super().__init__(statusStr)