import configparser
import pathlib


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URI:  postgresql://username:password@domain:port/database
file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

URL = config.get('DB', 'URL')

engine = create_engine(URL, echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
