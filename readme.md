# CxHistoricalDataGrabber

Program to download a given timeframe of historical data from the CxEngage API.

## Setup

1. Supply `tenant_id` in `config.json`.
2. Supply `tenant_region` in `config.json` – this is the region of your CxEngage instance. Either `Europe` or `North America`. Case sensitive.
2. Supply API credentials in `config.json`. This should be a `key`/`secret`.
3. Supply the desired `start_date` and `end_date` in `config.json`. These should be in ISO 8601 format, e.g. `2020-01-01T00:00:00Z`. If these are left blank, _all_ records from the tenant will be downloaded.
<!-- 4. *Optional* – Supply `limit` and `offset` in `config.json` to limit the number of records returned by the API. The default (0) will download all records in the given timeframe. The `offset` is used to paginate through the results if you are using, or have used, a `limit`. Be aware that downloading all records in a given timeframe may take a long time (~30 minutes per year of data). -->

Sample `config.json`:

```json
{
    "tenant_id": "08w3yfg3u4f032hg-e0g-340gh3-g34gh-33434d",
    "tenant_region": "Europe",
    "auth": {
        "key": "90r123e4gh-9132-44j4-g7ad-278934872fg98",
        "secret": "a0sdfy0whfpouwer09fgsdiugegr="
    },
    "start_date": "",
    "end_date": ""
}
```

## Usage

Please note, this program requires a lot of manual python script running. It does everything but all the scripts are not quite connected up in the way they should be to make this a single run-and-forget process.
