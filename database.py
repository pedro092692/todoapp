from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
from flask_security.models import fsqla_v3 as fsqla
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
