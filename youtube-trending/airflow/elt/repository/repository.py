from abc import abstractmethod

from elt.config.config import Config


class Repository:
    @abstractmethod
    def __init__(self, config: Config):
        self.username = config.USERNAME
        self.password = config.PASSWORD
        self.host = config.HOST
        self.port = config.PORT
        self.dbname = config.DBNAME
        self.POSTGRES_ENGINE_URL = f'postgresql+psycopg2://{config.USERNAME}:{config.PASSWORD}@{config.HOST}:{config.PORT}/{config.DBNAME}'