import os
import dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

Base = declarative_base()


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    link = Column(String)


class Content(Base):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True)
    text = Column(String(1000))
    image_id = Column(String(1000))


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    login = Column(String(100))
    password = Column(String(100))
    is_blocked = Column(Boolean, default=False)


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'))
    account_id = Column(Integer, ForeignKey('account.id'))
    content_id = Column(Integer, ForeignKey('content.id'))
    is_executed = Column(Boolean, default=False)
    execution_status = Column(Text, default=None)


# Создание строки подключения
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def select_group_by_id(group_id: int):
    session = Session()
    try:
        return session.query(Group).get(group_id)
    except SQLAlchemyError as e:
        print(f"Error selecting group: {e}")
    finally:
        session.close()


def select_account_by_id(account_id: int):
    session = Session()
    try:
        return session.query(Account).get(account_id)
    except SQLAlchemyError as e:
        print(f"Error selecting group: {e}")
    finally:
        session.close()


def select_content_by_id(content_id: int):
    session = Session()
    try:
        return session.query(Content).get(content_id)
    except SQLAlchemyError as e:
        print(f"Error selecting group: {e}")
    finally:
        session.close()


def select_tasks():
    session = Session()
    try:
        return session.query(Task).filter_by(execution_status='Подготовлена').all()
    except SQLAlchemyError as e:
        return []
    finally:
        session.close()



def set_task_status(task_id, new_status):
    session = Session()
    try:
        task = session.query(Task).get(task_id)
        if task:
            task.execution_status = new_status
            session.commit()
            print(f"Task {task_id} status updated to {new_status}")
        else:
            print(f"Task {task_id} not found")
    except SQLAlchemyError as e:
        print(f"Error updating task status: {e}")
        session.rollback()
    finally:
        session.close()


def mark_bad_account(account_id):
    session = Session()
    try:
        account = session.query(Account).get(account_id)
        if account:
            account.is_blocked = True
            session.commit()
            print(f"Account {account_id} marked as blocked")
        else:
            print(f"Account {account_id} not found")
    except SQLAlchemyError as e:
        print(f"Error marking account as blocked: {e}")
        session.rollback()
    finally:
        session.close()
