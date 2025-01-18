from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default='pending', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Пример подключения к базе данных SQLite
engine = create_engine('sqlite:///tasks.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class TaskRepository:
    def __init__(self):
        self.session = Session()

    def create_task(self, title, description=None):
        new_task = Task(title=title, description=description)
        self.session.add(new_task)
        self.session.commit()
        print(f"Создана задача: {new_task.title} (ID: {new_task.id})")
        return new_task

    def read_task(self, task_id):
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if task:
            print(f"Задача (ID: {task.id}): {task.title}, Статус: {task.status}, Описание: {task.description}")
            return task
        else:
            print("Задача не найдена.")
            return None

    def update_task(self, task_id, title=None, description=None, status=None):
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if task:
            if title:
                task.title = title
            if description:
                task.description = description
            if status:
                task.status = status
            self.session.commit()
            print(f"Обновлена задача (ID: {task.id}): {task.title}, Статус: {task.status}")
            return task
        else:
            print("Задача не найдена.")
            return None

    def delete_task(self, task_id):
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if task:
            self.session.delete(task)
            self.session.commit()
            print(f"Удалена задача (ID: {task.id}): {task.title}")
            return True
        else:
            print("Задача не найдена.")
            return False

# Пример использования класса TaskRepository
if __name__ == "__main__":
    repository = TaskRepository()
    # Создание задачи
    #created_task = repository.create_task("Изучить SQLAlchemy", "Изучить основные функции SQLAlchemy для работы с базами данных.")
    # Чтение задачи
    #repository.read_task(created_task.id)
    # Обновление задачи
    #repository.update_task(created_task.id, status="in_progress")
    # Удаление задачи
    repository.delete_task(1)
