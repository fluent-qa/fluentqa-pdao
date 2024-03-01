class RecordNotFoundException(RuntimeError):
    pass


class DAOException(RuntimeError):
    pass


class DBNotPreparedError(Exception):
    """
    DB Not Prepared Error
    """
