from .models import Product


class ProductRepository:
    def get_page(self, page: int, size: int):
        offset = (page - 1) * size
        return Product.objects.all()[offset:offset + size]

    def count_all(self) -> int:
        return Product.objects.count()

    def get_by_id(self, product_id):
        return Product.objects.filter(id=product_id).first()

    def exists_by_company_and_barcode(self, company_id, barcode: str) -> bool:
        return Product.objects.filter(company_id=company_id, barcode=barcode).exists()

    def create(self, company_id, barcode: str, name: str):
        return Product.objects.create(company_id=company_id, barcode=barcode, name=name)