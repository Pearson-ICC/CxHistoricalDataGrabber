from db.db import Database
from db.cxRecord import CxRecord
from typing import Generator, Any
import json


def recordsFromJsons(
    jsonLines: list[dict[str, Any]]
) -> Generator[CxRecord, None, None]:
    for line in jsonLines:
        record = CxRecord.fromDict(line, failSilent=True)
        if record is None:
            continue
        yield record


def setupDatabase():
    print("Reading records from file...")
    jsonString = (
        open("records.jsonl")
        .read()
        .strip()
        .replace(" ", "")
        .replace("\n", "")
        .replace("\t", "")
    )
    print("Processing file contents...")
    jsonLines = jsonString.split("}{")
    jsonLines[0] = jsonLines[0][1:]
    jsonLines[-1] = jsonLines[-1][:-1]
    jsonLines = ["{" + line + "}" for line in jsonLines]

    print(f"Compiling results into single dataset...")
    results: list[dict[str, Any]] = []
    for line in [json.loads(line) for line in jsonLines]:
        results.extend(line["results"])

    print(f"Compiled {len(results)} records.")
    print("Creating database...")
    records = recordsFromJsons(results)

    db = Database()
    db.insertAll(records)
    db.close()


setupDatabase()
