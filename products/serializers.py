from rest_framework import serializers
from .models import Product
from .messages import Messages


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'company_id', 'barcode', 'name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        validators = []


class ProductListQuerySerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1, min_value=1)
    size = serializers.IntegerField(required=False, default=20, min_value=1)

    def validate_size(self, value):
        if value > 100:
            raise serializers.ValidationError(Messages.SIZE_TOO_LARGE)
        return value