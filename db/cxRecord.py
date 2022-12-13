from datetime import datetime
from typing import Any


class CxRecord:
    interactionId: str  # interaction ID
    startTimestamp: datetime  # start time of the interaction
    interactionTime: int  # in seconds
    queue: str  # queue ID
    channelType: str  # voice | chat

    def __init__(
        self,
        interactionId: str,
        startTimestamp: datetime,
        interactionTime: int,
        queue: str,
        channelType: str,
    ):
        self.interactionId = interactionId
        self.startTimestamp = startTimestamp
        self.interactionTime = interactionTime
        self.queue = queue
        self.channelType = channelType

    @staticmethod
    def fromDict(_dict: dict[str, Any]):
        if "queues" not in _dict:
            raise ValueError("No queue found in record")
        if "interactionTime" not in _dict:
            raise ValueError("No interaction time found in record")

        record = CxRecord(
            interactionId=_dict["interactionId"],
            startTimestamp=datetime.fromisoformat(_dict["startTimestamp"][:-5]),
            interactionTime=_dict["interactionTime"],
            queue=_dict["queues"][0]["queueId"],
            channelType=_dict["channelType"],
        )

        return record


# TODO: just process EO UK queue
