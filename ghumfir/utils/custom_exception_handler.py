from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated

from ghumfir.utils.exceptions import *
import logging, traceback

def log(exc):
    logging.error(type(exc))
    logging.error(traceback.format_exc())

def custom_exception_handler(exc, context):
    if(isinstance(exc, NotAuthenticated)):
        exc = MyUnAuthenticatedError(str(exc))
        
    if(not issubclass(type(exc), MyExceptions) or isinstance(exc, MyConfigurationError)):
        log(exc)
    print(exc)
    print(type(exc))
    print(issubclass(type(exc), MyExceptions))
    if(not issubclass(type(exc), MyExceptions)):
        try:
            exc = MySomethingWentWrong(str(exc))
        except:
            exc = MySomethingWentWrong("Could not connect to the server")
    exception = {
        "data": {},
        "errors": exc.args[0],
        "status_code": exc.status_code,
        "code_name": exc.default_code
    }
    return Response(exception, status = exc.status_code)
    