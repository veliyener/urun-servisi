import pytest
from clients.company_client import CompanyClient, CompanyClientError
from .services import (
    ProductService,
    ProductNotFoundError,
    CompanyPassiveError,
    CompanyServiceUnavailableError,
)


@pytest.mark.django_db
def test_olmayan_id_ile_urun_istendiginde_hata_firlar():
    service = ProductService()

    with pytest.raises(ProductNotFoundError):
        service.get_product("00000000-0000-0000-0000-000000000000")


class FakeCompanyClient:
    def __init__(self, company_data=None, should_raise=False):
        self.company_data = company_data
        self.should_raise = should_raise

    def get_company(self, company_id):
        if self.should_raise:
            raise CompanyClientError("Firma servisine ulasilamiyor.")
        return self.company_data


@pytest.mark.django_db
def test_pasif_firmaya_urun_eklenmeye_calisilirsa_hata_firlar_bagimlilik_enjeksiyonu_ile():
    fake_client = FakeCompanyClient(company_data={"id": "x", "title": "Sahte Firma", "status": "passive"})
    service = ProductService(company_client=fake_client)

    with pytest.raises(CompanyPassiveError):
        service.create_product(company_id="00000000-0000-0000-0000-000000000000", barcode="1111111111111", name="Test")


@pytest.mark.django_db
def test_firma_servisine_ulasilamadiginda_urun_eklenemez(monkeypatch):
    def fake_get_company(self, company_id):
        raise CompanyClientError("Firma servisine ulasilamiyor.")

    monkeypatch.setattr(CompanyClient, "get_company", fake_get_company)

    service = ProductService()
    with pytest.raises(CompanyServiceUnavailableError):
        service.create_product(company_id="00000000-0000-0000-0000-000000000000", barcode="2222222222222", name="Test")