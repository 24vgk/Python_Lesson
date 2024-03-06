from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, \
    ForeignKey
from datetime import datetime


from Config_data.config import Config, load_config


config: Config = load_config()


def engine():
    # engine = create_engine(f"mysql+pymysql://root:{config.db.db_password}@localhost/{config.db.database}", echo=True)
    engine = create_engine('sqlite:///LESSON.db')
    metadata = MetaData()
    users = Table(
        'users',
        metadata,
        Column('Id', Integer(), unique=True, primary_key=True),
        Column('User_id', Integer(), unique=True, nullable=False),
        Column('First_name', String(100), nullable=False),
        Column('User_name', String(100), nullable=False),
        Column('Is_admin', Boolean(), default=False),
        Column('Is_block', Boolean(), default=False),
        Column('Create_user', DateTime(), default=datetime.now())
    )
    metadata.create_all(engine)
    return engine

