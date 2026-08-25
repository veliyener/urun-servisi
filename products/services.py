from .repositories import ProductRepository
from .messages import Messages


class DuplicateBarcodeError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


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

    def get_product(self, product_id):
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(Messages.PRODUCT_NOT_FOUND)
        return product

    def create_product(self, company_id, barcode: str, name: str):
        if self.repository.exists_by_company_and_barcode(company_id, barcode):
            raise DuplicateBarcodeError(Messages.BARCODE_ALREADY_EXISTS_FOR_COMPANY)
        return self.repository.create(company_id, barcode, name)