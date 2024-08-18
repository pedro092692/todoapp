from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, func, and_
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
from flask_security.models import fsqla_v3 as fsqla
from datetime import datetime
from typing import List
import os


# create DB
class Base(DeclarativeBase):
    pass


# create extension
db = SQLAlchemy(model_class=Base)
fsqla.FsModels.set_db_info(db)


# configure tables
class Role(db.Model, fsqla.FsRoleMixin):
    pass


class User(db.Model, fsqla.FsUserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    fs_uniquifier: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    tasks: Mapped[List["Task"]] = relationship(order_by="Task.id.desc()")


class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    sub_tasks: Mapped[List["SubTask"]] = relationship(order_by="SubTask.id.desc()")

    @staticmethod
    def create_task(user_id, title):
        new_task = Task(
            user_id=user_id,
            title=title
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task

    @staticmethod
    def get_task(task_id):
        task = db.get_or_404(Task, task_id)
        return task

    @staticmethod
    def search(user_id, query):
        task = db.session.execute(db.select(Task).filter(
            Task.user_id == user_id, Task.title.icontains(query)
        ).order_by(Task.id.desc())).scalars().all()
        return task


class SubTask(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("task.id"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class DataBase:

    def __init__(self, app):
        self.db = db
        self.app = app

        # setup flask security
        self.user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        self.app.security = Security(self.app, self.user_datastore)

        # database init
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
        self.app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECRET_KEY')

        self.db.init_app(self.app)

    def create_tables(self):
        with self.app.app_context():
            self.db.create_all()
