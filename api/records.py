from typing import Any, Generator
from api.apiConfig import API
import json


class Records:
    def __init__(self, api: API) -> None:
        self.__api = api

    def getSingleRecordSet(self, start: str, end: str, offset: int) -> dict[Any, Any]:
        """Connects to the API and returns one result set.
        This is usually 1000 records.

        Args:
            `start` (`str`): The start date for the query - ISO8601 format e.g. 2021-01-01T00:00:00.000Z
            `end` (`str`): The end date for the query - ISO8601 format
            `offset` (`int`): The offset to use for the API call - offset of 10 means start at record 10 etc.

        Returns:
            `dict[Any, Any]`: The result set from the API
        """
        url = f"interactions?start={start}&end={end}&limit=1000&offset={offset}"
        response = self.__api.get(url)
        return response.json()

    def getAllRecords(self, offset: int = 0) -> Generator[dict[Any, Any], None, None]:
        """Repeatedly calls `getSingleRecordSet`, incrementing the `offset` by 1000 each time until all records are retrieved.

        Args:
            `offset` (`int`): The offset to use for the API call - offset of 10 means start at record 10 etc.

        Yields:
            `dict[Any, Any]`: The result set from the API
        """
        while True:
            result = self.getSingleRecordSet(
                self.__api.start_date, self.__api.end_date, offset
            )
            yield result
            if len(result["results"]) < 1000:
                break
            offset += 1000

    def appendRecords(self, records: dict[Any, Any], file_path: str) -> None:
        """Appends the records to a file of existing JSON records

        Args:
            `records` (`dict[Any, Any]`): The records to save
            `file_path` (`str`): The path to the file to save to
        """
        with open(file_path, "a") as file:
            json.dump(records, file)
