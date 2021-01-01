import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

# local_path = os.path.dirname(__file__)
database = "todo.db"
# db_file = os.path.join(local_path, database)
db_engine = f'sqlite:///{database}?check_same_thread=False'
# print(db_engine)

engine = create_engine(db_engine)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
today = datetime.today().date()

class Tasks(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today().date())

    def __init__(self, task, deadline):
         self.task = task
         self.deadline = deadline


Base.metadata.create_all(engine)


def add_task(session, tache, date_limite=today):
    new_row = Tasks(task=tache, deadline=date_limite)
    session.add(new_row)
    session.commit()


def delete_task(session, to_delete):
    row = session.query(Tasks) \
        .filter(Tasks.id == to_delete) \
        .all()
    specific_row = row[0]
    session.delete(specific_row)
    session.commit()


def get_today_tasks(session):
    rows = session.query(Tasks) \
        .filter(Tasks.deadline == today) \
        .all()
    return rows


def get_tasks_by_day(session, day):
    rows = session.query(Tasks) \
        .filter(Tasks.deadline == day) \
        .all()
    return rows


def get_week_tasks(session):
    rows = session.query(Tasks) \
        .filter(Tasks.deadline >= today) \
        .filter(Tasks.deadline <= today + timedelta(days=6)) \
        .order_by(Tasks.deadline) \
        .all()
    return rows


def get_all_tasks(session):
    rows = session.query(Tasks) \
        .order_by(Tasks.deadline) \
        .all()
    return rows

def get_missed_tasks(session):
    rows = session.query(Tasks) \
        .filter(Tasks.deadline < today) \
        .order_by(Tasks.deadline) \
        .all()
    return rows


def print_today_tasks(session):
    tasks = list(get_today_tasks(session))
    print(f'\nToday {today.strftime("%-d %b")}:')
    if len(tasks) == 0:
        print_nothing()
    else:
        i = 1
        for task in tasks:
            print(f'{i}. {task.task}')
            i+= 1


def print_week_tasks(session):
    weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in [today + timedelta(days=nb) for nb in range(7)]:
        print(f'\n{weekday[day.weekday()]} {day.strftime("%-d %b")}:')
        tasks = get_tasks_by_day(session, day)
        if len(tasks) == 0:
            print_nothing()
        else:
            i = 1
            for task in tasks:
                print(f'{i}. {task.task}')
                i += 1


def print_all_tasks(session):
    tasks = get_all_tasks(session)
    print('\nAll tasks:')
    if len(tasks) == 0:
        print_nothing()
    else:
        i = 1
        for task in tasks:
            print(f'{i}. {task.task}. {task.deadline.strftime("%-d %b")}')
            i += 1


def print_create_task(session):
    print('Enter task')
    tache = input()
    print('Enter deadline')
    limite = input().split('-')
    date_limite = None if limite == [''] else datetime(int(limite[0]), int(limite[1]), int(limite[2]))
    add_task(session, tache, date_limite)
    print('The task has been added!')
    print()


def print_missed_tasks(session):
    tasks = get_missed_tasks(session)
    print('\nMissed tasks:')
    if len(tasks) == 0:
        print_nothing()
    else:
        i = 1
        for task in tasks:
            print(f'{i}. {task.task}. {task.deadline.strftime("%-d %b")}')
            i += 1


def print_delete_task(session):
    tasks = get_all_tasks(session)
    print('\nChoose the number of the task you want to delete:')
    task_list = []
    to_delete = 0
    if len(tasks) == 0:
        print_nothing()
    else:
        i = 1
        for task in tasks:
            print(f'{i}. {task.task}. {task.deadline.strftime("%-d %b")}')
            task_list.append(task.id)
            i += 1
        to_delete = task_list[int(input()) - 1]
        delete_task(session, to_delete)
        print('The task has been deleted!')


def print_nothing():
    print('Nothing to do!')


# __main__


menu = """
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit"""
reponse = 1

while reponse != 0:
    print(menu)
    reponse = input()
    if not reponse.isdigit or int(reponse) == 0:
        reponse = 0
    elif int(reponse) == 1:
        print_today_tasks(session)
    elif int(reponse) == 2:
        print_week_tasks(session)
    elif int(reponse) == 3:
        print_all_tasks(session)
    elif int(reponse) == 4:
        print_missed_tasks(session)
    elif int(reponse) == 6:
        print_delete_task(session)
    else:
        print_create_task(session)
