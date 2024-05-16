class ApiExceptionCase(Exception):
    def __init__(self, status_code: int, context: dict):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context


class ApiException(object):
    class FedWrongURL(ApiExceptionCase):
        def __init__(self, context: dict = None):
            ApiExceptionCase.__init__(self, 400, context)
