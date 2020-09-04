class FatalError(Exception):
    """
    FatalError indicates a fatal error. If a fatal error is encountered,
    make halts, prints the message and exits with a non zero exit code.
    """
    def __init__(self, message, code=1):
        self.message = message
        self.code = code
