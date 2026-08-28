import uuid
from django.db import models


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_id = models.UUIDField(db_index=True)
    company_title = models.CharField(max_length=255, blank=True, default='')
    barcode = models.CharField(max_length=13)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        constraints = [
            models.UniqueConstraint(fields=['company_id', 'barcode'], name='unique_barcode_per_company')
        ]

    def __str__(self):
        return self.name