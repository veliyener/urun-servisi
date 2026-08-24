from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, ProductListQuerySerializer
from .services import ProductService


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

        data = self.service.list_products(page=page, size=size)
        serializer = ProductSerializer(data['results'], many=True)
        return Response({
            'total': data['total'],
            'page': data['page'],
            'size': data['size'],
            'results': serializer.data,
        })

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = self.service.create_product(
            company_id=serializer.validated_data['company_id'],
            barcode=serializer.validated_data['barcode'],
            name=serializer.validated_data['name'],
        )
        result = ProductSerializer(product)
        return Response(result.data, status=status.HTTP_201_CREATED)