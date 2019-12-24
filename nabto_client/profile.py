from nabto_client import nabto_api as api
from nabto_client.exception import check_status, check_result


class NabtoProfile:
    @staticmethod
    @check_status
    def createProfile(email: str, password: str):
        return api.nabto_create_profile(email, password)

    @staticmethod
    @check_status
    def createSelfSignedProfile(id: str, password: str):
        return api.nabto_create_self_signed_profile(id, password)

    @staticmethod
    @check_status
    def removeProfile(id: str):
        return api.nabto_remove_profile(id)

    @staticmethod
    @check_result
    def getFingerprint(id: str):
        return api.nabto_get_fingerprint(id)
