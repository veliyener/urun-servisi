from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, ProductListQuerySerializer
from .messages import Messages
from .services import (
    ProductService,
    DuplicateBarcodeError,
    ProductNotFoundError,
    CompanyNotFoundError,
    CompanyPassiveError,
    CompanyServiceUnavailableError,
)


class ProductListCreateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductService()

    def get_serializer(self, *args, **kwargs):
        return ProductSerializer(*args, **kwargs)

    def get(self, request):
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

    def post(self, request):
        if not request.headers.get('X-User-Id'):
            return Response({'detail': Messages.USER_ID_REQUIRED}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            product = self.service.create_product(
                company_id=serializer.validated_data['company_id'],
                barcode=serializer.validated_data['barcode'],
                name=serializer.validated_data['name'],
            )
        except CompanyServiceUnavailableError as e:
            return Response({'detail': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except CompanyNotFoundError as e:
            return Response({'company_id': [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
        except CompanyPassiveError as e:
            return Response({'company_id': [str(e)]}, status=status.HTTP_409_CONFLICT)
        except DuplicateBarcodeError as e:
            return Response({'barcode': [str(e)]}, status=status.HTTP_409_CONFLICT)
        result = ProductSerializer(product)
        return Response(result.data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductService()

    def get_serializer(self, *args, **kwargs):
        return ProductSerializer(*args, **kwargs)

    def get(self, request, id):
        try:
            product = self.service.get_product(id)
        except ProductNotFoundError as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def delete(self, request, id):
        try:
            self.service.delete_product(id)
        except ProductNotFoundError as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)