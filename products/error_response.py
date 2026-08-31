from rest_framework.response import Response


def error_response(code: str, message: str, status_code: int, field: str = None):
    body = {
        "error": {
            "code": code,
            "message": message,
        }
    }
    if field:
        body["error"]["details"] = {"field": field}
    return Response(body, status=status_code)