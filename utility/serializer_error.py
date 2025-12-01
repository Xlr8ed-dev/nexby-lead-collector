def serializer_error(serializer_errors):
    messages = [
        "{error}".format(error=str(error))
        for _, errors in serializer_errors.items()
        for error in errors
    ]
    return messages
