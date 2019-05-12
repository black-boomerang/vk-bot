from create_db import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('group.group_id', ondelete='CASCADE'), default=1)
    admin_flg = Column(Boolean, default=False)

    def __repr__(self):
        return "<User(user_id={}, group_id={}, admin_flg={})>".format(self.user_id, self.group_id, self.admin_flg)


class Group(Base):
    __tablename__ = 'group'

    group_id = Column(Integer, primary_key=True)
    university_nm = Column(String)
    faculty_nm = Column(String)
    group_nm = Column(String)

    def __repr__(self):
        return "<Group(group_id={}, university_nm={}, faculty_nm={}, group_nm={})>".format(self.group_id,
                                                                                           self.university_nm,
                                                                                           self.faculty_nm,
                                                                                           self.group_nm)


class ScheduleRequest(Base):
    __tablename__ = 'schedule_request'

    request_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'))
    schedule_dt = Column(Date, ForeignKey('schedule_date.schedule_dt', ondelete='CASCADE'))

    def __repr__(self):
        return "<ScheduleRequest(request_id={}, user_id={}, schedule_dt={})>".format(self.request_id, self.user_id,
                                                                                     self.schedule_dt)


class ScheduleDate(Base):  # потребовалось для нормализации БД
    __tablename__ = 'schedule_date'

    schedule_dt = Column(Date, primary_key=True)

    def __repr__(self):
        return "<ScheduleDate(schedule_dt={})>".format(self.schedule_dt)


class Schedule(Base):
    __tablename__ = 'schedule'

    group_id = Column(Integer, ForeignKey('group.group_id', ondelete='CASCADE'), primary_key=True)
    schedule_dt = Column(Date, ForeignKey('schedule_date.schedule_dt', ondelete='CASCADE'), primary_key=True)
    schedule_inf = Column(String)

    def __repr__(self):
        return "<Schedule(group_id={}, schedule_dt={}, schedule_inf={})>".format(self.group_id, self.schedule_dt,
                                                                                 self.schedule_inf)
