from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

import json

# Loading credentials

with open("./Configuration.json") as file:
    __CREDENTIALS = json.load(file)

if __CREDENTIALS is None:
    raise Exception("Problems connecting to the database")

__engine : Engine = create_engine(f"mysql+pymysql://{__CREDENTIALS['User']}:{__CREDENTIALS['Pass']}@{__CREDENTIALS['Host']}:{__CREDENTIALS['Port']}/repComun",
                                  pool_recycle=3600,
                                  pool_timeout=180)

SESSIONMAKER = sessionmaker(__engine)

class RepComunBase(DeclarativeBase):
    pass
