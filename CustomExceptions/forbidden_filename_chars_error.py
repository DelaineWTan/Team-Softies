class ForbiddenFilenameCharsError(Exception):
    def __init__(self, message = 'Cannot use forbidden characters in filenames.') -> None:
        self.message = message
        super().__init__(self.message)
