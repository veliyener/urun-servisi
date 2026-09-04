from rest_framework.views import exception_handler

TRANSLATIONS = {
    "Must be a valid UUID.": "Geçerli bir UUID olmalıdır.",
    "This field is required.": "Bu alan zorunludur.",
    "This field may not be blank.": "Bu alan boş bırakılamaz.",
    "A valid integer is required.": "Geçerli bir sayı olmalıdır.",
}


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        errors = response.data
        first_field = next(iter(errors), None)
        first_message = str(errors[first_field][0]) if first_field else "Geçersiz istek."
        first_message = TRANSLATIONS.get(first_message, first_message)

        response.data = {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": first_message,
                "details": {"field": first_field} if first_field else None,
            }
        }
    return response