from db.importer import Importer
from db.db import Database


def importJsonToDb():
    RECORDS_PATH = "/Users/felixweber/Documents/CxHistoricalDataGrabber/records.jsonl"

    importer = Importer(RECORDS_PATH)
    allResults = importer.importAll()

    db = Database()
    db.insertFromGenerator(allResults)


db = Database()
results = db.getWhere(queueId="856d61e0-3c18-11e8-ab44-d9904d0e6e43")
