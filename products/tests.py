import pytest
from clients.company_client import CompanyClient
from .services import ProductService, ProductNotFoundError, CompanyPassiveError, CompanyServiceUnavailableError


@pytest.mark.django_db
def test_olmayan_id_ile_urun_istendiginde_hata_firlar():
    service = ProductService()

    with pytest.raises(ProductNotFoundError):
        service.get_product("00000000-0000-0000-0000-000000000000")


@pytest.mark.django_db
def test_pasif_firmaya_urun_eklenmeye_calisilirsa_hata_firlar(monkeypatch):
    def fake_get_company(self, company_id):
        return {"id": company_id, "title": "Sahte Firma", "status": "passive"}

    monkeypatch.setattr(CompanyClient, "get_company", fake_get_company)

    service = ProductService()
    with pytest.raises(CompanyPassiveError):
        service.create_product(company_id="00000000-0000-0000-0000-000000000000", barcode="1111111111111", name="Test")


@pytest.mark.django_db
def test_firma_servisine_ulasilamadiginda_urun_eklenemez(monkeypatch):
    def fake_get_company(self, company_id):
        from clients.company_client import CompanyClientError
        raise CompanyClientError("Firma servisine ulaşılamıyor.")

    monkeypatch.setattr(CompanyClient, "get_company", fake_get_company)

    service = ProductService()
    with pytest.raises(CompanyServiceUnavailableError):
        service.create_product(company_id="00000000-0000-0000-0000-000000000000", barcode="2222222222222", name="Test")