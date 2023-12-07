class InputLengthError(Exception):
    def __init__(self, message = 'Given input is too long for this context.') -> None:
        self.message = message
        super().__init__(self.message)