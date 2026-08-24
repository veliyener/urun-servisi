from .repositories import ProductRepository


class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def list_products(self, page: int = 1, size: int = 20):
        products = self.repository.get_page(page, size)
        total = self.repository.count_all()
        return {
            'total': total,
            'page': page,
            'size': size,
            'results': products,
        }

    def create_product(self, company_id, barcode: str, name: str):
        return self.repository.create(company_id, barcode, name)