from db.mock import Mock
from db.user import User
from db.db_session import create_session

def get_user(user_id: int):
    with create_session() as session:
        return session.query(User).filter(User.id == user_id).first()
    
def create_user(user: User):
    with create_session() as session:
        session.add(user)
        session.commit()

def update_user(user: User):
    with create_session() as session:
        session.merge(user)
        session.commit()

def get_mock(index: int):
    with create_session() as session:
        return session.query(Mock).filter(Mock.id == (index+1)).first()
    
def delete_user(user_id: int):
    with create_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            session.delete(user)
            session.commit()