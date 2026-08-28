import requests
from decouple import config


class CompanyClient:
    BASE_URL = config('COMPANY_SERVICE_URL')
    TIMEOUT = 2

    def get_company(self, company_id):
        url = f"{self.BASE_URL}/{company_id}"
        response = requests.get(url, timeout=self.TIMEOUT)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()