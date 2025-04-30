import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(DSN):
    global __factory

    if __factory:
        return

    engine = sa.create_engine(DSN, echo=True)
    __factory = orm.sessionmaker(bind=engine)

    from .__all_models import Mock, default_mocks, User

    SqlAlchemyBase.metadata.create_all(engine)

    with create_session() as session:
        mocks = session.query(Mock).all()
        if not mocks:
            session.add_all(default_mocks)
            session.commit()


def create_session() -> Session:
    global __factory
    return __factory()