import nabto_client.nabto as nabto

class NabtoProfile:
    @staticmethod
    def createSelfSignedProfile(id: str, password: str):
        return nabto.nabtoCreateSelfSignedProfile(id, password)

    @staticmethod
    def removeProfile(id: str):
        return nabto.nabtoRemoveProfile(id)

    @staticmethod
    def getFingerprint(id: str):
        return nabto.nabtoGetFingerprint(id)
