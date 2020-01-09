import nabto_client.nabto as nabto

def createSelfSignedProfile(id: str, password: str):
    return nabto.nabtoCreateSelfSignedProfile(id, password)

def removeProfile(id: str):
    return nabto.nabtoRemoveProfile(id)

def getFingerprint(id: str):
    return nabto.nabtoGetFingerprint(id)
