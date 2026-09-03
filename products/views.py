from typing import Optional
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, ProductListQuerySerializer
from .messages import Messages, ErrorCodes
from .error_response import error_response
from .services import (
    ProductService,
    DuplicateBarcodeError,
    ProductNotFoundError,
    CompanyNotFoundError,
    CompanyPassiveError,
    CompanyServiceUnavailableError,
)


class ProductListCreateView(APIView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.service = ProductService()

    def get_serializer(self, *args, **kwargs):
        return ProductSerializer(*args, **kwargs)

    def get(self, request) -> Response:
        query_serializer = ProductListQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        page = query_serializer.validated_data['page']
        size = query_serializer.validated_data['size']
        company_id = query_serializer.validated_data['company_id']

        data = self.service.list_products(page=page, size=size, company_id=company_id)
        serializer = ProductSerializer(data['results'], many=True)
        return Response({
            'total': data['total'],
            'page': data['page'],
            'size': data['size'],
            'results': serializer.data,
        })

    def post(self, request) -> Response:
        if not request.headers.get('X-User-Id'):
            return error_response(
                ErrorCodes.USER_ID_REQUIRED, Messages.USER_ID_REQUIRED, status.HTTP_401_UNAUTHORIZED
            )

        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            product = self.service.create_product(
                company_id=serializer.validated_data['company_id'],
                barcode=serializer.validated_data['barcode'],
                name=serializer.validated_data['name'],
            )
        except CompanyServiceUnavailableError as e:
            return error_response(
                ErrorCodes.COMPANY_SERVICE_UNAVAILABLE, str(e), status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except CompanyNotFoundError as e:
            return error_response(
                ErrorCodes.COMPANY_NOT_FOUND, str(e), status.HTTP_400_BAD_REQUEST, field="company_id"
            )
        except CompanyPassiveError as e:
            return error_response(
                ErrorCodes.COMPANY_PASSIVE, str(e), status.HTTP_409_CONFLICT, field="company_id"
            )
        except DuplicateBarcodeError as e:
            return error_response(
                ErrorCodes.DUPLICATE_BARCODE, str(e), status.HTTP_409_CONFLICT, field="barcode"
            )
        result = ProductSerializer(product)
        return Response(result.data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.service = ProductService()

    def get_serializer(self, *args, **kwargs):
        return ProductSerializer(*args, **kwargs)

    def get(self, request, id) -> Response:
        try:
            product = self.service.get_product(id)
        except ProductNotFoundError as e:
            return error_response(ErrorCodes.PRODUCT_NOT_FOUND, str(e), status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def delete(self, request, id) -> Response:
        try:
            self.service.delete_product(id)
        except ProductNotFoundError as e:
            return error_response(ErrorCodes.PRODUCT_NOT_FOUND, str(e), status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)