from datetime import datetime
from typing import Any, Optional


class CxRecord:
    interactionId: str  # interaction ID
    startTimestamp: datetime  # start time of the interaction
    interactionTime: int  # in seconds
    customer: str  # customer ID
    queue: str  # queue ID
    channelType: str  # voice | chat

    def __init__(
        self,
        interactionId: str,
        startTimestamp: datetime,
        interactionTime: int,
        customer: str,
        queue: str,
        channelType: str,
    ):
        self.interactionId = interactionId
        self.interactionTime = interactionTime
        if type(startTimestamp) == datetime:
            self.startTimestamp = startTimestamp
        else:
            self.startTimestamp = datetime.fromisoformat(startTimestamp)  # type: ignore
        self.customer = customer
        self.queue = queue
        self.channelType = channelType

    @staticmethod
    def fromDict(
        _dict: dict[str, Any], failSilent: bool = False
    ) -> Optional["CxRecord"]:
        if "queues" not in _dict:
            if failSilent:
                return None
            raise ValueError("No queue found in record")
        if "interactionTime" not in _dict:
            if failSilent:
                return None
            raise ValueError("No interaction time found in record")

        record = CxRecord(
            interactionId=_dict["interactionId"],
            startTimestamp=datetime.fromisoformat(_dict["startTimestamp"][:-5]),
            interactionTime=_dict["interactionTime"],
            customer=_dict["customer"],
            queue=_dict["queues"][0]["queueId"],
            channelType=_dict["channelType"],
        )

        return record
