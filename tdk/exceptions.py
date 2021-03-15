class TdkPyException(Exception):
    pass


class TdkErrorException(TdkPyException):
    responsible_endpoint = "TDK"

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        if self.message is not None:
            return f"{self.responsible_endpoint} responded with an error: {self.message}"
        return f"{self.responsible_endpoint} responded with an error."


class TdkUnexpectedResponseException(TdkPyException):
    responsible_endpoint = "TDK"

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        if self.message is not None:
            return f"Unexpected or malformed response from {self.responsible_endpoint}: {self.message}"
        return f"Unexpected or malformed response from {self.responsible_endpoint}"


class TdkSearchErrorException(TdkErrorException):
    responsible_endpoint = "TDK GTS Search"


class TdkSearchUnexpectedResponseException(TdkUnexpectedResponseException):
    responsible_endpoint = TdkSearchErrorException.responsible_endpoint


class TdkIdLookupErrorException(TdkErrorException):
    responsible_endpoint = "TDK GTS Reverse ID Lookup"


class TdkIdLookupUnexpectedResponseException(TdkUnexpectedResponseException):
    responsible_endpoint = TdkIdLookupErrorException.responsible_endpoint
