from sqlalchemy import create_engine, MetaData, Column, Integer, String, ForeignKey, select, case, event, func
from sqlalchemy.orm import sessionmaker, relation, aliased
from sqlalchemy.ext.declarative import declarative_base
from sqlamp import DeclarativeMeta
from app import Config


engine = create_engine('postgresql+psycopg2://'+Config.DB_USER+'@'+Config.DB_HOST+':'+Config.DB_PORT+'/'+Config.DB_NAME)
metadata = MetaData(engine)
Session = sessionmaker(bind=engine)

Base = declarative_base(metadata=metadata, metaclass=DeclarativeMeta)
