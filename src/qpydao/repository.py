from qpydao import DatabaseConfig
from qpydao import Databases


class BaseRepository:
    def __init__(self, config: DatabaseConfig = None):
        self.db_client = Databases.default_client(config)
