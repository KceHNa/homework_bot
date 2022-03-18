from xmlrpc.client import ResponseError


class DateError(Exception):
    pass


class NotListOrDict(TypeError):
    pass


class ResponseNoKey(TypeError):
    pass


class EndpointNotAvailable(ResponseError):
    pass


class ResponseApiError(ResponseError):
    pass
