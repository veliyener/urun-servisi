import requests
from .repositories import ProductRepository
from .messages import Messages
from clients.company_client import CompanyClient


class DuplicateBarcodeError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


class CompanyNotFoundError(Exception):
    pass


class CompanyPassiveError(Exception):
    pass


class CompanyServiceUnavailableError(Exception):
    pass


class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
        self.company_client = CompanyClient()

    def list_products(self, page: int = 1, size: int = 20, company_id=None):
        products = self.repository.get_page(page, size, company_id)
        total = self.repository.count_all(company_id)
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
        try:
            company = self.company_client.get_company(company_id)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            raise CompanyServiceUnavailableError(Messages.COMPANY_SERVICE_UNAVAILABLE)

        if company is None:
            raise CompanyNotFoundError(Messages.COMPANY_NOT_FOUND)
        if company['status'] != 'active':
            raise CompanyPassiveError(Messages.COMPANY_PASSIVE)

        if self.repository.exists_by_company_and_barcode(company_id, barcode):
            raise DuplicateBarcodeError(Messages.BARCODE_ALREADY_EXISTS_FOR_COMPANY)
        return self.repository.create(company_id, barcode, name)

    def delete_product(self, product_id):
        product = self.get_product(product_id)
        self.repository.delete(product)