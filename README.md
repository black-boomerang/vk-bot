﻿Реализован бот, помогающий пользователю просматривать расписание занятий. Через бота можно как узнать расписание, так и изменить
его (подтвердив права администратора). Данные хранятся в базе данных, находящейся на сервере. В качестве сервера был выбран сервер
Heroku (адрес страницы https://tranquil-lake-72776.herokuapp.com/ ). Всю необходимую для пользователя информацию можно запросить
у бота командой 'help'. 
В файле app.py обрабатываются запросы от ВК. 
Файл run.py запускает приложение на сервере.
В файле messsage_handler.py содержатся все вспомогательные функции для обработки сообщений пользователя.
В базе находятся пять таблиц: User, Group, Schedule, ScheduleDate, ScheduleRequest (одна из них ScheduleDate добавлена
для нормализации базы данных). Все классы этих таблиц находятся в файле db_classes.py. Сами таблицы создавались на сервере при
помощи файла create_db.py.
Все ключи и токены содержатся в файле settings.py.
Файл select.py нужен, чтобы просматривать содержимое базы данных на сервере.
Репозиторий на github является полной копией репозитория на Heroku.
Проверить роботоспособность бота можно на таком примере:
	ВУЗ: МФТИ
	Факультет: ФИВТ
	Группа: Б05-827
	День занятий: 13.05.2019

Ссылка на бота: https://vk.com/club181818843
Ключ администратора: iamadmin
