import requests


class CompanyClient:
    BASE_URL = "http://localhost:8000/api/v1/companies"

    def get_company(self, company_id):
        url = f"{self.BASE_URL}/{company_id}"
        response = requests.get(url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()