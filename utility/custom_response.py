from rest_framework.response import Response


def create_response(
        status_code, success=None, message=None, errors=None, *args, **kwargs
):
    data = {"status": status_code}
    if success is not None:
        data["success"] = success
    if message is not None:
        data["message"] = message
    if errors is not None:
        data["error"] = errors

    if kwargs:
        for key, value in kwargs.items():
            data[key] = value

    return Response(data, status=status_code)
