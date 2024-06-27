class RecordNotFoundException(RuntimeError):
    pass


class DAOException(RuntimeError):
    pass


class DatabaseClientConfigError(Exception):
    """
    Database Configuration is not ready
    """
