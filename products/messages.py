class ErrorCodes:
    DUPLICATE_BARCODE = "DUPLICATE_BARCODE"
    PRODUCT_NOT_FOUND = "PRODUCT_NOT_FOUND"
    COMPANY_NOT_FOUND = "COMPANY_NOT_FOUND"
    COMPANY_PASSIVE = "COMPANY_PASSIVE"
    COMPANY_SERVICE_UNAVAILABLE = "COMPANY_SERVICE_UNAVAILABLE"
    USER_ID_REQUIRED = "USER_ID_REQUIRED"
    VALIDATION_ERROR = "VALIDATION_ERROR"


class Messages:
    BARCODE_ALREADY_EXISTS_FOR_COMPANY = "Bu barkod, bu firma için zaten kayıtlı."
    SIZE_TOO_LARGE = "size en fazla 100 olabilir."
    PRODUCT_NOT_FOUND = "Böyle bir ürün bulunamadı."
    COMPANY_NOT_FOUND = "Belirtilen firma bulunamadı."
    COMPANY_PASSIVE = "Bu firma pasif durumda, ürün eklenemez."
    COMPANY_SERVICE_UNAVAILABLE = "Firma bilgisi şu anda doğrulanamıyor, lütfen birazdan tekrar deneyin."
    USER_ID_REQUIRED = "Bu işlem için X-User-Id başlığı zorunludur."