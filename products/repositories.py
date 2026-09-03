from typing import Optional
from .models import Product


class ProductRepository:
    def get_page(self, page: int, size: int, company_id: Optional[str] = None):
        queryset = Product.objects.all()
        if company_id is not None:
            queryset = queryset.filter(company_id=company_id)
        offset = (page - 1) * size
        return queryset[offset:offset + size]

    def count_all(self, company_id: Optional[str] = None) -> int:
        queryset = Product.objects.all()
        if company_id is not None:
            queryset = queryset.filter(company_id=company_id)
        return queryset.count()

    def get_by_id(self, product_id: str) -> Optional[Product]:
        return Product.objects.filter(id=product_id).first()

    def exists_by_company_and_barcode(self, company_id: str, barcode: str) -> bool:
        return Product.objects.filter(company_id=company_id, barcode=barcode).exists()

    def create(self, company_id: str, company_title: str, barcode: str, name: str) -> Product:
        return Product.objects.create(
            company_id=company_id,
            company_title=company_title,
            barcode=barcode,
            name=name,
        )

    def delete(self, product: Product) -> None:
        product.delete()