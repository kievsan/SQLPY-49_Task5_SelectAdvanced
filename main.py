# [SQLPY-49] 5. Музыкальный сервис
# к лекции «Группировки, выборки из нескольких таблиц» 25.03.2022
# ДЗ Написать SELECT-запросы и вывести информацию


import time
import psycopg2
import sqlalchemy
import pandas as pd

from tables_tools import create_tables
from tables_tools import create_relations
from tables_tools import drop_tables

from data import get_data
from tasks import get_tasks


def connect_to_db(login, password, db_name):
    if "" in (login.strip(), password, db_name.strip()):
        print('Недостаточно данных для работы с базой данных!')
        quit(1)
    db = f'postgresql+psycopg2://{login}:{password}@localhost:5432/{db_name}'
    engine = sqlalchemy.create_engine(db)
    return {'database': db, 'engine': engine}


if __name__ == '__main__':
    connect_about = connect_to_db('py49', '123456', 'py49_db')
    db_scheme = 'sqlpy49_task3_1'
    connection = connect_about['engine'].connect()
    connection.execute(f"SET SCHEMA '{db_scheme}';")

    print('\n\t Заполним базу данных:\n'
          '==============================================================\n')
    drop_tables(connection)
    create_tables(connection)
    create_relations(connection)
    for data in get_data():
        executed = connection.execute(data['select'])
        print(data['task'], data['select'])
        # time.sleep(5)

    print('\n\t ЗАДАНИЕ: '
          '\n\t Написать SELECT-запросы 1) - 9) и вывести информацию\n'
          '==============================================================\n')
    for task in get_tasks():
        executed = connection.execute(task['select'])
        print(task['task'], task['select'])
        print(pd.DataFrame(executed))
        print()

    connection.close()
