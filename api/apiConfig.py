from typing import Optional, Any
import requests


class API:
    __base_url: str

    tenant_id: str
    token: Optional[str]
    apiKey: Optional[str]
    apiSecret: Optional[str]
    start_date: str
    end_date: str

    @staticmethod
    def from_json(json_data: dict[str, Any]) -> "API":
        return API(
            tenant_id=json_data["tenant_id"],
            region=json_data["tenant_region"],
            apiKey=json_data["auth"]["key"],
            apiSecret=json_data["auth"]["secret"],
            start_date=json_data["start_date"],
            end_date=json_data["end_date"],
        )

    def __init__(
        self,
        tenant_id: str,
        region: str,
        apiKey: Optional[str],
        apiSecret: Optional[str],
        start_date: str,
        end_date: str,
    ) -> None:
        self.tenant_id = tenant_id
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.start_date = start_date
        self.end_date = end_date

        if region == "Europe":
            self.__base_url = "https://eu-west-1-prod-api.cxengage.net/v1"
        elif region == "North America":
            self.__base_url = "https://api.cxengage.net/v1"
        else:
            raise ValueError(
                f"Invalid region {region}. Must be 'Europe' or 'North America'"
            )

        self.refreshToken()

    def __str__(self) -> str:
        return f"APIConfig(tenant_id={self.tenant_id}, apiKey={self.apiKey}, apiSecret={self.apiSecret}, token={self.token}, start_date={self.start_date}, end_date={self.end_date})"

    @property
    def url(self) -> str:
        return f"{self.__base_url}/tenants/{self.tenant_id}/"

    @property
    def headers(self) -> dict[str, str]:
        return {"Authorization": f"Token {self.token}"}

    def refreshToken(self):
        body = {
            "username": self.apiKey,
            "password": self.apiSecret,
            "tenantId": self.tenant_id,
        }
        response = requests.post(
            f"{self.__base_url}/tokens",
            json=body,
            headers={"Content-Type": "application/json"},
        )
        print(f"Refreshed token {response.status_code}")
        self.token = response.json()["token"]

    def get(self, url: str) -> requests.Response:
        # print(f"{self.url}{url}")
        response = requests.get(
            f"{self.url}{url}",
            headers=self.headers,
        )
        if response.status_code == 401:
            self.refreshToken()
            response = requests.get(
                f"{self.url}{url}",
                headers=self.headers,
            )
        return response
