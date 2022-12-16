from api.apiConfig import API
from typing import Any
import json


def getQueueMapping(api: API) -> dict[str, str]:
    """Get a mapping of queue names to queue IDs"""
    queues: str = api.get("queues").content  # type: ignore
    queues: list[dict[str, Any]] = json.loads(queues)["result"]  # type: ignore # changing the type of queues variable
    return {queue["id"]: queue["name"] for queue in queues}


with open("config.json", "r") as file:
    config = json.load(file)
api = API.from_json(config)
queue_mapping = getQueueMapping(api)

with open("queueIdNameMap.json", "w") as file:
    json.dump(queue_mapping, file)
