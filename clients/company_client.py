from typing import Optional
import requests
from decouple import config, UndefinedValueError
from products.messages import Messages


class CompanyClientError(Exception):
    pass


class CompanyClientConfigurationError(Exception):
    pass


class CompanyClient:
    TIMEOUT = 2

    def __init__(self) -> None:
        try:
            self.base_url = config('COMPANY_SERVICE_URL')
        except UndefinedValueError:
            raise CompanyClientConfigurationError(
                "COMPANY_SERVICE_URL ortam degiskeni tanimli degil."
            )

    def get_company(self, company_id: str) -> Optional[dict]:
        url = f"{self.base_url}/{company_id}"
        try:
            response = requests.get(url, timeout=self.TIMEOUT)
            if response.status_code == 404:
                return None
            response.raise_for_status()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError):
            raise CompanyClientError(Messages.COMPANY_CLIENT_UNREACHABLE)

        return response.json()