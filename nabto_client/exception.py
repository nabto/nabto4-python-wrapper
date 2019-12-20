from nabto_client.nabto_api import nabto_status_str, Status


class NabtoException(Exception):
    def __init__(self, status, message=None):
        statusStr = nabto_status_str(status)
        if message:
            super().__init__("{}: {}".format(statusStr, message))
        else:
            super().__init__(statusStr)


def check_status(function):
    def wrapper(*args, **kwargs):
        status = function(*args, **kwargs)

        if status != Status.NABTO_OK:
            raise NabtoException(status)

        return status

    return wrapper


def check_result(function):
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)

        if result.status != Status.NABTO_OK:
            raise NabtoException(result.extra)

        return result.extra

    return wrapper
