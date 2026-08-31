from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        errors = response.data
        first_field = next(iter(errors), None)
        first_message = errors[first_field][0] if first_field else "Geçersiz istek."

        response.data = {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": str(first_message),
                "details": {"field": first_field} if first_field else None,
            }
        }
    return response