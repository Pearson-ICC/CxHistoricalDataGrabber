import json


def getQueueIDToNameMapping() -> dict[str, str]:
    FILE_PATH = "queueIdNameMap.json"
    with open(FILE_PATH, "r") as f:
        return json.load(f)


def getAllQueueIDs() -> list[str]:
    return list(getQueueIDToNameMapping().keys())
