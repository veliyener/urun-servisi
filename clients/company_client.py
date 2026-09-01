import requests
from products.messages import Messages


class CompanyClientError(Exception):
    pass


class CompanyClient:
    BASE_URL = "http://localhost:8000/api/v1/companies"
    TIMEOUT = 2

    def get_company(self, company_id):
        url = f"{self.BASE_URL}/{company_id}"
        try:
            response = requests.get(url, timeout=self.TIMEOUT)
            if response.status_code == 404:
                return None
            response.raise_for_status()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError):
            raise CompanyClientError(Messages.COMPANY_CLIENT_UNREACHABLE)

        return response.json()