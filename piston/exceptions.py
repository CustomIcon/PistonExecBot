  
class Error(Exception):
    pass


class UnsupportedLanguage(Error):
    pass


class EndpointDown(Error):
    pass