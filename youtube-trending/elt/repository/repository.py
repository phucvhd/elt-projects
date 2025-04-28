from abc import abstractmethod

from config.config import Config


class Repository:
    @abstractmethod
    def __init__(self, config: Config):
        self.username = config.username
        self.password = config.password
        self.host = config.host
        self.port = config.port
        self.dbname = config.dbname
        self.POSTGRES_ENGINE_URL = f'postgresql+psycopg2://{config.username}:{config.password}@{config.host}:{config.port}/{config.dbname}'