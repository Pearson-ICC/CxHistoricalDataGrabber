from db.importer import Importer
from db.db import Database


def importJsonToDb():
    RECORDS_PATH = "/Users/felixweber/Documents/CxHistoricalDataGrabber/records.jsonl"

    importer = Importer(RECORDS_PATH)
    allResults = importer.importAll()

    db = Database()
    db.insertFromGenerator(allResults)


def importFromDb():
    db = Database()
    results = db.getAll()
    print(len(results))


# importJsonToDb()
importFromDb()
