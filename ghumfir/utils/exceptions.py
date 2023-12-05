class MyExceptions(Exception):
    pass

class MyBadRequest(MyExceptions):
    status_code = 400
    default_detail = 'The supposed case was not handled on the frontend'
    default_code = 'bad_request'

class MyConfigurationError(MyExceptions):
    status_code = 501
    default_detail = 'Implemented improperly'
    default_code = 'not_implemented'

class MyValidationError(MyExceptions):
    status_code = 403
    default_detail = 'Validation error for the provided request'
    default_code = 'validation_error'

class MyUnAuthenticatedError(MyExceptions):
    status_code = 401
    default_detail = 'The user needs to be authenticated to make the request'
    default_code = 'unauthenticated_user'

class MySomethingWentWrong(MyExceptions):
    status_code = 500
    default_detail = 'All unhandled exceptions'
    default_code = 'something_went_wrong'
