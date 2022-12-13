from db.db import Database
from datetime import datetime, timedelta
from typing import Generator
from db.cxRecord import CxRecord


def roundToChunkSize(timestamp: datetime, chunk_size: timedelta) -> datetime:
    """Round a timestamp down to the nearest chunk_size."""
    # 1. convert all stuff to timestamps (seconds since epoch)
    # 2. get the remainder of the timestamp divided by the chunk size (in seconds)
    # 3. subtract that remainder from the timestamp
    # 4. convert back to datetime

    if chunk_size == timedelta(hours=24):
        # hack to make sure we're rounding down to the nearest day. otherwise, we'll get
        # weird results like 2022-12-01 01:00:00 due to daylight savings time
        timestamp = datetime(timestamp.year, timestamp.month, timestamp.day)
        return timestamp

    rounded = datetime.fromtimestamp(
        timestamp.timestamp() - (timestamp.timestamp() % chunk_size.total_seconds()),
    )

    return rounded


def mapRecordByRoundingTimestampDownToChunk(
    record: CxRecord, chunk_size: timedelta
) -> Generator[tuple[str, datetime, str, int, int], None, None]:
    """Map a record to a time chunk by rounding the timestamp down to the nearest chunk."""
    # round down record.startTimestamp to nearest chunk_size
    yield (
        record.queue,
        roundToChunkSize(record.startTimestamp, chunk_size),
        record.customer,
        record.interactionTime,
        1,
    )


def createIndividualChunkData(
    chunk_size: timedelta,
    records: Generator[CxRecord, None, None],
) -> Generator[tuple[str, datetime, str, int, int], None, None]:
    """
    Create a list of tuples containing the following data:
    - queueID
    - startTimestamp
    - customer
    - avgHandleTime
    - contactCount
    """

    for record in records:
        yield from mapRecordByRoundingTimestampDownToChunk(record, chunk_size)


def generateChunkedDateTimes(
    start: datetime, end: datetime, chunk_size: timedelta
) -> Generator[datetime, None, None]:
    """Generate a list of datetime objects split into chunks of chunk_size."""
    current = start
    while current < end:
        yield current
        current += chunk_size


def aggregate(
    chunk_size: timedelta, c: list[tuple[str, datetime, str, int, int]]
) -> dict[datetime, list[tuple[str, datetime, str, int, int]]]:
    START_DATE = c[-1][1]
    END_DATE = c[0][1]
    # swap start and end date if they're the wrong way around
    if START_DATE > END_DATE:
        START_DATE, END_DATE = END_DATE, START_DATE  # type: ignore
    END_DATE += chunk_size  # type: ignore
    START_DATE = roundToChunkSize(START_DATE, chunk_size)  # type: ignore
    END_DATE = roundToChunkSize(END_DATE, chunk_size)  # type: ignore

    chunkedDateTimes = list(generateChunkedDateTimes(START_DATE, END_DATE, chunk_size))
    chunkData: dict[datetime, list[tuple[str, datetime, str, int, int]]] = {
        chunk: [] for chunk in chunkedDateTimes
    }

    for chunk in c:
        chunkData[chunk[1]].append(chunk)

    return chunkData


# split into 15 min chunks
# get:
# - average interaction time for each time chunk
# - number of interactions for each time chunk
# - number of contacts handled for each time chunk

db = Database()
records = db.getAll()
CHUNK_SIZE = timedelta(minutes=15)

chunks = list(createIndividualChunkData(CHUNK_SIZE, records))
aggregatedChunkData = aggregate(CHUNK_SIZE, chunks)

print("Calculating statistics")

statistics = {}
for chunk in aggregatedChunkData.keys():
    if len(aggregatedChunkData[chunk]) == 0:
        statistics[chunk] = {
            "avgInteractionTime": 0,
            "numInteractions": 0,
            "numContacts": 0,
        }
        continue

    # calculate average interaction time for aggregatedChunkData[chunk]
    avgInteractionTime = sum(
        [record[3] for record in aggregatedChunkData[chunk]]
    ) / len(aggregatedChunkData[chunk])
    # calculate number of interactions for aggregatedChunkData[chunk]
    numInteractions = len(aggregatedChunkData[chunk])
    # calculate number of unique contacts handled for aggregatedChunkData[chunk]
    numContacts = len(set([record[2] for record in aggregatedChunkData[chunk]]))

    statistics[chunk] = {
        "avgInteractionTime": avgInteractionTime,
        "numInteractions": numInteractions,
        "numContacts": numContacts,
    }

print(statistics)
