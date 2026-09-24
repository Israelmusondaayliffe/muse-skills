class CitizenForgeError(Exception):
    """Base error with a beginner-safe message."""


class ValidationError(CitizenForgeError):
    pass


class PolicyError(CitizenForgeError):
    pass


class TransitionError(CitizenForgeError):
    pass


class StorageError(CitizenForgeError):
    pass
