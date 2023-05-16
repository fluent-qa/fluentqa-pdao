from qpydao import DatabaseClient, DatabaseConfig


class BaseRepository(DatabaseClient):

    def __init__(self, config: DatabaseConfig = None):
        super().__init__(config)
