from xmlrpc.client import ResponseError


class NotListOrDict(TypeError):
    pass


class ResponseNoKey(TypeError):
    pass


class EndpointNotAvailable(ResponseError):
    pass


class ResponseApiError(ResponseError):
    pass


class TelegramSendError(Exception):
    pass
