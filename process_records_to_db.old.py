from db.db import Database
from datetime import datetime, timedelta
from typing import Generator
from db.cxRecord import CxRecord


def generateChunkedDateTimes(
    start: datetime, end: datetime, chunk_size: timedelta
) -> Generator[datetime, None, None]:
    """Generate a list of datetime objects split into chunks of chunk_size."""
    current = start
    while current < end:
        yield current
        current += chunk_size


def createIndividualChunkData(
    chunk_size: timedelta,
    start_date: datetime,
    end_date: datetime,
    records: Generator[CxRecord, None, None],
) -> list[tuple[str, datetime, str, int, int]]:
    """
    Create a list of tuples containing the following data:
    - queueID
    - startTimestamp
    - customer
    - avgHandleTime
    - contactCount
    """

    print("Starting processing")
    processedData = list[
        tuple[str, datetime, str, int, int]
    ]()  # queueID, startTimestamp, customer, avgHandleTime, contactCount

    dateTimeChunks = generateChunkedDateTimes(start_date, end_date, chunk_size)

    def mapRecord(
        record: CxRecord,
        chunk_size: timedelta,
    ) -> Generator[tuple[str, datetime, str, int, int], None, None]:
        for timeChunk in dateTimeChunks:
            if timeChunk <= record.startTimestamp < timeChunk + chunk_size:
                # record is in this time chunk
                yield (
                    record.queue,
                    timeChunk,
                    record.customer,
                    record.interactionTime,
                    1,
                )
                # records.remove(record)
                continue

    def mapRecordByRoundingTimestampDownToChunk(
        record: CxRecord, chunk_size: timedelta
    ) -> Generator[tuple[str, datetime, str, int, int], None, None]:
        """Map a record to a time chunk by rounding the timestamp down to the nearest chunk."""
        # round down record.startTimestamp to nearest chunk_size
        def roundToChunkSize(timestamp: datetime, chunk_size: timedelta) -> datetime:
            """Round a timestamp down to the nearest chunk_size."""
            # 1. convert all stuff to timestamps (seconds since epoch)
            # 2. get the remainder of the timestamp divided by the chunk size (in seconds)
            # 3. subtract that remainder from the timestamp
            # 4. convert back to datetime
            return datetime.fromtimestamp(
                timestamp.timestamp()
                - (timestamp.timestamp() % chunk_size.total_seconds()),
            )

        yield (
            record.queue,
            roundToChunkSize(record.startTimestamp, chunk_size),
            record.customer,
            record.interactionTime,
            1,
        )

    # start a timer (time how long this takes)
    start = datetime.now()

    i = 0
    max_i = 10000
    for record in records:
        i += 1
        if i > max_i:
            break
        for chunk in mapRecordByRoundingTimestampDownToChunk(record, chunk_size):
            processedData.append(chunk)

    # end timer
    end = datetime.now()

    for timeChunk in processedData:
        print(f"{timeChunk} - {len(processedData)}")

    print(
        f"Time taken for {max_i} records: {end - start} seconds ({(end - start) / max_i}s per record)"
    )

    return processedData


# split into half hour chunks
# get:
# - average interaction time for each half hour
# - number of interactions for each half hour
# - number of contacts handled for each half hour

db = Database()
records = db.getAll()

CHUNK_SIZE = timedelta(minutes=15)
START_DATE = datetime(2018, 1, 1)
END_DATE = datetime(2022, 12, 10)

chunks = createIndividualChunkData(CHUNK_SIZE, START_DATE, END_DATE, records)
print(chunks)

# [
#     print(a)
#     for a in generateChunkedDateTimes(
#         datetime(2021, 1, 1), datetime(2022, 1, 1), CHUNK_SIZE
#     )
# ]
