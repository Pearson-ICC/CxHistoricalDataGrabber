import json
from db.cxRecord import CxRecord
from typing import Generator


class Importer:
    def __init__(self, path: str):
        self.path = path

    def importResultSet(self, _json: str) -> Generator[CxRecord, None, None]:
        for record in json.loads(_json)["results"]:
            try:
                yield CxRecord.fromDict(record)
            except ValueError:
                pass  # no queue/interaction time found in record, do not import

    def importAll(self) -> Generator[CxRecord, None, None]:
        with open(self.path) as recordsFile:
            for jsonLine in recordsFile:
                for result in self.importResultSet(jsonLine):
                    yield result

    def importByQueueId(self, queueId: str) -> Generator[CxRecord, None, None]:
        with open(self.path) as recordsFile:
            for jsonLine in recordsFile:
                for result in self.importResultSet(jsonLine):
                    if result.queue == queueId:
                        yield result
