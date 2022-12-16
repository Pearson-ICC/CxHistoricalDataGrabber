from typing import Any
from datetime import datetime
from typing import Generator


def statsToCsv(
    stats: dict[datetime, Any],
    intervalDuration: str,
    queueIDMap: dict[str, str],
    continueWriting: bool,
) -> None:
    # stats format is:
    # {
    #    "avgInteractionTime": int,
    #    "numInteractions": int,
    #    "numContacts": int,
    # }

    # convert to csv in format:
    # {
    #    "QueueName": str,
    #    "QueueId": str,
    #    "ChannelType": str,
    #    "TimeStamp": str, (iso8601, x min chunked)
    #    "IntervalDuration": str,
    #    "IncomingContactVolume": int,
    #    "AverageHandleTime": int,
    #    "ContactsHandled": int,
    # }

    headers = [
        "QueueName",
        "QueueId",
        "ChannelType",
        "TimeStamp",
        "IntervalDuration",
        "IncomingContactVolume",
        "AverageHandleTime",
        "ContactsHandled",
    ]

    headers = ",".join(headers)

    def genLines() -> Generator[str, None, None]:
        for chunk, value in stats.items():
            yield ",".join(
                [
                    queueIDMap[value["queueId"]],
                    value["queueId"],
                    "VOICE",
                    chunk.isoformat(),
                    intervalDuration,
                    str(int(value["numInteractions"])),
                    str(int(value["avgInteractionTime"])),
                    str(int(value["numContacts"])),
                ]
            )

    if continueWriting:
        with open("stats.csv", "a") as f:
            f.write("\n".join(genLines()) + "\n")
    else:
        with open("stats.csv", "w") as f:
            f.write(headers + "\n")
            f.write("\n".join(genLines()) + "\n")
