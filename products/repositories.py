from .models import Product


class ProductRepository:
    def get_page(self, page: int, size: int, company_id=None):
        queryset = Product.objects.all()
        if company_id is not None:
            queryset = queryset.filter(company_id=company_id)
        offset = (page - 1) * size
        return queryset[offset:offset + size]

    def count_all(self, company_id=None) -> int:
        queryset = Product.objects.all()
        if company_id is not None:
            queryset = queryset.filter(company_id=company_id)
        return queryset.count()

    def get_by_id(self, product_id):
        return Product.objects.filter(id=product_id).first()

    def exists_by_company_and_barcode(self, company_id, barcode: str) -> bool:
        return Product.objects.filter(company_id=company_id, barcode=barcode).exists()

    def create(self, company_id, barcode: str, name: str):
        return Product.objects.create(company_id=company_id, barcode=barcode, name=name)

    def delete(self, product):
        product.delete()