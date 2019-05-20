from db_classes import User, Group, Schedule, ScheduleRequest
from create_db import DB_Session


def func():
    db_session = DB_Session()
    '''group = Group(university_nm='МФТИ')
    db_session.add(group)
    db_session.commit()
    d = {'university_nm': 'МФТИ', 'faculty_nm': None, 'group_nm': None}
    group = db_session.query(Group).filter_by(**d).first()'''
    res = db_session.query(User).all()
    print(str(res))
    res = db_session.query(Group).all()
    print(str(res))
    res = db_session.query(Schedule).all()
    print(str(res))
    res = db_session.query(ScheduleRequest).all()
    print(str(res))


func()
