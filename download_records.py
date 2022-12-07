from api.records import Records
from api.apiConfig import API
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


records = Records(getAPI("config.json"))

api = getAPI("config.json")
for record in records.getAllRecords():
    print(
        f"{record['offset']} of {record['total']} fetched ({record['offset'] / record['total'] * 100:.2f}%)"
    )
    records.appendRecords(record, "records.json")
