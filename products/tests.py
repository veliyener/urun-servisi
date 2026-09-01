import pytest
from .services import ProductService, ProductNotFoundError


@pytest.mark.django_db
def test_olmayan_id_ile_urun_istendiginde_hata_firlar():
    service = ProductService()

    with pytest.raises(ProductNotFoundError):
        service.get_product("00000000-0000-0000-0000-000000000000")