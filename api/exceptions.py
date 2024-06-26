class TokenNotFoundException(Exception):
    def __init__(self, message="Token was not found in the HTML page"):
        self.message = message
        super().__init__(self.message)


class DataNotFoundException(Exception):
    def __init__(self, message="The data was not found"):
        self.message = message
        super().__init__(self.message)
