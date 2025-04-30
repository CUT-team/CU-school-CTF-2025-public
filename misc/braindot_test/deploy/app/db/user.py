import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase

class User(SqlAlchemyBase):
    __tablename__ = "users"
    
    id:int = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, unique=True, index=True)
    register_time:datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now)
    username:str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    first_name:str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    last_name:str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    bio:str = sqlalchemy.Column(sqlalchemy.String, nullable=True)