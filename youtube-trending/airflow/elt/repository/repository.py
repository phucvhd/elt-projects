from abc import abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from elt.config.config import Config

import logging

logger = logging.getLogger(__name__)

class Repository:
    @abstractmethod
    def __init__(self, config: Config):
        self.username = config.USERNAME
        self.password = config.PASSWORD
        self.host = config.HOST
        self.port = config.PORT
        self.dbname = config.DBNAME
        self.POSTGRES_ENGINE_URL = f'postgresql+psycopg2://{config.USERNAME}:{config.PASSWORD}@{config.HOST}:{config.PORT}/{config.DBNAME}'
        self.engine = create_engine(self.POSTGRES_ENGINE_URL)
    
    def get_session(self):
        logger.info(f"Creating database session")
        return Session(self.engine)
