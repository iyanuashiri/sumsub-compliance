class SumsubError(Exception):
    def __init__(self, message: str, status_code: int = None):
        """
        Constructor for MonoError
        :param message: The reason for the error.
        :param status_code: THe status
        """
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f"{self.status_code} {self.message}"

    def __repr__(self):
        return f"{self.__class__.__name__}, {self.message}, {self.status_code}"