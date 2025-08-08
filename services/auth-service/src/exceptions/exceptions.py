from typing import Optional

class AnalysisException(Exception):
    pass

class NotFoundException(AnalysisException):
    def __init__(self, resource: str, identifier: str):
        self.resource = resource
        self.identifier = identifier

class UnauthorizedException(AnalysisException):
    def __init__(self, message: str = "Unauthorized"):
        self.message = message

class OperationFailedException(AnalysisException):
    def __init__(self, message: str = "For unknown reasons, the operation failed."):
        self.message = message

class ListFailedException(AnalysisException):
    def __init__(self, message: str = "There was a problem with the list.", list_object: str = "list"):
        self.message = message
        self.list_object = list_object


class AuthorisationException(Exception):
    pass

class TokenExpiredException(AuthorisationException):
    def __init__(self, message: str = "Your JWT has expired. Please request a new Token."):
        self.message = message

class WrongLoginDataException(AuthorisationException):
    def __init__(self, message: str = "Wrong Credentials; the username or password provided by you are wrong."):
        self.message = message

# Exceptions (default exceptions, that are universally used)
class MissingValueException(Exception):
    def __init__(self, missing_variable: str, message: str = "is Missing"):
        self.missing_variable = missing_variable
        self.message = message

class WrongInputException(Exception):
    def __init__(self, wrong_variables: str, documentation: str = "logically false Argument(s)"):
        self.wrong_variables = wrong_variables
        self.documentation = documentation

class DivisionByZeroException(Exception):
    def __init__(self, function: Optional[str] = None, divisor: Optional[str] = None): # str = "not specified", divisor: str = "not specified"):
        self.function = function
        self.divisor = divisor