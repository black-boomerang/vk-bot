import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(os.environ['DATABASE_URL'])
DB_Session = sessionmaker(bind=engine)
db_session = DB_Session()
Base = declarative_base()

if __name__ == '__main__':
    from db_classes import Base, User, Group, ScheduleDate, Schedule, ScheduleRequest

    Base.metadata.drop_all(bind=engine, tables=[Schedule.__table__, ScheduleRequest.__table__, ScheduleDate.__table__,
                                                User.__table__, Group.__table__])
    Base.metadata.create_all(bind=engine)
    db_session.add(Group())
    db_session.commit()
