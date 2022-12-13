from db.db import Database
from datetime import datetime, timedelta
from typing import Generator
from db.cxRecord import CxRecord

db = Database()
results = list(db.getAll())

# split into half hour chunks
# get:
# - average interaction time for each half hour
# - number of interactions for each half hour
# - number of contacts handled for each half hour


def generateChunkedDateTimes(
    start: datetime, end: datetime, chunk_size: timedelta
) -> Generator[datetime, None, None]:
    """Generate a list of datetime objects split into chunks of chunk_size."""
    current = start
    while current < end:
        yield current
        current += chunk_size


CHUNK_SIZE = timedelta(minutes=15)
START_DATE = datetime(2021, 1, 1)
END_DATE = datetime(2022, 12, 10)

chunks: dict[datetime, set[CxRecord]] = {}
for chunk in generateChunkedDateTimes(START_DATE, END_DATE, CHUNK_SIZE):
    chunks[chunk] = set()

print("Starting processing")

# start a timer
start = datetime.now()

i = 0
max_i = 5000
for result in results:
    i += 1
    if i > max_i:
        break
    for chunk in chunks:
        # print(result.startTimestamp)
        if chunk <= result.startTimestamp < chunk + CHUNK_SIZE:
            chunks[chunk].add(result)
            results.remove(result)
            continue

# end timer
end = datetime.now()

for chunk in chunks:
    print(f"{chunk} - {len(chunks[chunk])}")

print(
    f"Time taken for {max_i} records: {end - start} seconds ({(end - start) / max_i}s per record)"
)

# [
#     print(a)
#     for a in generateChunkedDateTimes(
#         datetime(2021, 1, 1), datetime(2022, 1, 1), CHUNK_SIZE
#     )
# ]
