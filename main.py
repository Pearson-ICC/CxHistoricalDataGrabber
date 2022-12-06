from typing import Any, Generator
from apiConfig import API
import json


def getAPI(file_path: str) -> API:
    """Reads the config file and returns the APIConfig object

    Args:
        `file_path` (`str`): The path to the config file

    Returns:
        `APIConfig`: The APIConfig object
    """

    with open(file_path, "r") as file:
        config = json.load(file)
    return API.from_json(config)


def getSingleRecordSet(api: API, start: str, end: str, offset: int) -> dict[Any, Any]:
    """Connects to the API and returns one result set.
    This is usually 1000 records.

    Args:
        `apiConfig` (`APIConfig`): The configuration for the API
        `start` (`str`): The start date for the query - ISO8601 format e.g. 2021-01-01T00:00:00.000Z
        `end` (`str`): The end date for the query - ISO8601 format
        `offset` (`int`): The offset to use for the API call - offset of 10 means start at record 10 etc.

    Returns:
        `dict[Any, Any]`: The result set from the API
    """
    url = f"interactions?start={start}&end={end}&limit=1000&offset={offset}"
    response = api.get(url)
    return response.json()


def getAllRecords(api: API) -> Generator[dict[Any, Any], None, None]:
    """Repeatedly calls `getSingleRecordSet`, incrementing the `offset` by 1000 each time until all records are retrieved.

    Args:
        `apiConfig` (`APIConfig`): The configuration for the API

    Yields:
        `dict[Any, Any]`: The result set from the API
    """
    offset = 0
    while True:
        result = getSingleRecordSet(api, api.start_date, api.end_date, offset)
        yield result
        if len(result["results"]) < 1000:
            break
        offset += 1000


def appendRecords(records: dict[Any, Any], file_path: str) -> None:
    """Appends the records to a file of existing JSON records

    Args:
        `records` (`dict[Any, Any]`): The records to save
        `file_path` (`str`): The path to the file to save to
    """
    with open(file_path, "a") as file:
        json.dump(records, file)


api = getAPI("config.json")
for record in getAllRecords(api):
    print(
        f"{record['offset']} of {record['total']} fetched ({record['offset'] / record['total'] * 100:.2f}%)"
    )
    appendRecords(record, "records.json")
