import re
import datetime
from settings import admin_key
from db_classes import User, Group, ScheduleDate, ScheduleRequest, Schedule
from create_db import DB_Session


# получение справки
def get_help_text():
    text_file = open('help_text.txt', 'r')
    text = text_file.read()
    return text


# вставка новых данных в таблицы group и обновление данных в таблице user
def info_insertion(db_session, group_info, user):
    group = db_session.query(Group).filter_by(**group_info).first()
    if group is None:
        group = Group(**group_info)
        db_session.add(group)
        db_session.commit()
    user.group_id = group.group_id
    db_session.commit()


# получение объекта пользователя
def get_user(db_session, user_id):
    new_user_flg = False
    user = db_session.query(User).filter_by(user_id=user_id).first()
    if user is None:  # это первое сообщение от пользователя (добавляем его в БД)
        user = User(user_id=user_id)
        db_session.add(user)
        db_session.commit()
        new_user_flg = True
    return (user, new_user_flg)


# получить расписание
def get_schedule(db_session, group_id, schedule_dt):
    schedule = db_session.query(Schedule).filter_by(group_id=group_id, schedule_dt=schedule_dt).first()
    if schedule is None:
        return None
    schedule_text = schedule.schedule_inf
    return schedule_text


# изменить расписание
def change_schedule(db_session, group_id, schedule_dt, new_schedule):
    schedule = db_session.query(Schedule).filter_by(group_id=group_id, schedule_dt=schedule_dt).first()
    if schedule is None:
        schedule = Schedule(group_id=group_id, schedule_dt=schedule_dt)
        db_session.add(schedule)
    schedule.schedule_inf = new_schedule
    db_session.commit()


# добавление конкретного дня (потребовалось для нормализации БД)
def set_schedule_date(db_session, schedule_date):
    schedule_dt = db_session.query(ScheduleDate).filter_by(schedule_dt=schedule_date).first()
    if schedule_dt is None:
        schedule_dt = ScheduleDate(schedule_dt=schedule_date)
        db_session.add(schedule_dt)
        db_session.commit()


# создаём новый запрос дасписания для сбора статистики
def insert_new_request(db_session, user_id, schedule_dt):
    set_schedule_date(db_session, schedule_dt)
    schedule_request = ScheduleRequest(user_id=user_id, schedule_dt=schedule_dt)
    db_session.add(schedule_request)
    db_session.commit()


# проверка, ввёл пользователь ВУЗ или факультет или нет
def is_name(message):
    return (message.isupper()) and (len(message) <= 15)


# проверка, ввёл пользователь ВУЗ или факультет или нет
def is_group(message):
    return (re.search(r'\d', message) is not None) and (len(message) <= 15)


# обработка самого запроса
def request_handler(db_session, user, message):
    message = message.strip()

    # не зависмо от запроса сообщение должно содержать дату
    schedule_dt = re.search(r'\d{2}.\d{2}.\d{4}', message)
    if schedule_dt is None:
        return 'Запрос некорректен'

    schedule_dt = schedule_dt.group()
    message_array = re.split(schedule_dt, message)
    schedule_dt = datetime.datetime.strptime(schedule_dt, "%d.%m.%Y").date()

    getting_flg = message_array[0].strip().lower() == 'покажи расписание на'
    changing_flg = (message_array[0].strip().lower() == 'измени расписание на') and (user.is_admin is True)

    # пользователь не запрашивает и не пытается изменить расписание
    if getting_flg is False and changing_flg is False:
        return 'Запрос некорректен'

    if getting_flg is True:  # получение расписания
        insert_new_request(db_session, user.user_id, schedule_dt)  # создаём новый запрос для статистики
        schedule = get_schedule(db_session, user.group_id, schedule_dt)
        if schedule is None:
            return 'Нет информации о расписании на данный день'
        return schedule
    else:  # изменение расписания
        set_schedule_date(db_session, schedule_dt)
        new_schedule = message_array[1].strip()
        change_schedule(db_session, user.group_id, schedule_dt, new_schedule)
        return 'Расписание успешно изменено'


# обработчик сообщений
def message_handler(data):
    db_session = DB_Session()
    user_id = data['object']['user_id']
    original_message = data['object']['body']
    message = original_message.strip().lower()

    user, new_user_flg = get_user(db_session, user_id)

    message_array = message.split()

    if message_array[0] == 'help':  # получение справки
        if new_user_flg is True:
            db_session.delete(user)
            db_session.commit()
        text = get_help_text()
        return text
    elif message_array[0] == 'admin':  # пользователь хочет получить админские права
        if message_array[1] == admin_key:
            user.is_admin = True
            db_session.add(user)
            db_session.commit()
            return 'Права админа успешно подтверждены'
        return 'Неверный ключ'
    elif message_array[0] == 'delete':  # пользователь хочет удалиться из базы
        db_session.delete(user)
        db_session.commit()
        return 'Вы были успешно удалены из базы'

    if new_user_flg:  # первое сообщение от пользователя
        return 'Введи название ВУЗа'

    # находим группу пользователя в таблице group
    group = db_session.query(Group).filter_by(group_id=user.group_id).first()
    group_info = {'university_nm': group.university_nm, 'faculty_nm': group.faculty_nm,
                  'group_nm': group.group_nm}

    if group.university_nm is None:  # пользователь в сообщении указал ВУЗ
        if is_name(original_message):
            group_info['university_nm'] = message
            info_insertion(db_session, group_info, user)
            return 'Введи название факультета'
        return 'Запрос некорректен'

    if group.faculty_nm is None:  # пользователь в сообщении указал факультет
        if is_name(original_message):
            group_info['faculty_nm'] = message
            info_insertion(db_session, group_info, user)
            return 'Введи название(номер) группы'
        return 'Запрос некорректен'

    if group.group_nm is None:  # пользователь в сообщении указал группу
        if is_group(original_message):
            group_info['group_nm'] = message
            info_insertion(db_session, group_info, user)
            return 'Информация добавлена в базу'
        return 'Запрос некорректен'

    return request_handler(db_session, user, original_message)
