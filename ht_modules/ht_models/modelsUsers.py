print("- in modelsUsers")
# from .main import Base_users, sess_users
from .main import dict_base, dict_sess
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, \
    Date, Boolean, Table
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# from itsdangerous.serializer import Serializer
from itsdangerous.url_safe import URLSafeTimedSerializer
from datetime import datetime
from flask_login import UserMixin
from .config import config
import os
from flask import current_app

Base_users = dict_base['Base_users']
sess_users = dict_sess['sess_users']

def default_username(context):
    return context.get_current_parameters()['email'].split('@')[0]


class Users(Base_users, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    email = Column(Text, unique = True, nullable = False)
    username = Column(Text, default=default_username)
    password = Column(Text, nullable = False)
    admin = Column(Boolean, default=False)
    posts = relationship('BlogPosts', backref='author', lazy=True)
    # user_habit = relationship('HabitsRecorded', backref='user_habit_ref', lazy=True)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)
    habits = relationship("UserHabitAssociations", back_populates="users")
    habit_days = relationship('UserHabitDays', backref='habit_days_ref', lazy=True)

    def get_reset_token(self):

        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):

        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            payload = serializer.loads(token, max_age=1000)
            user_id = payload.get("user_id")
        except:
            return None

        return sess_users.query(Users).get(user_id)

    def __repr__(self):
        return f'Users(id: {self.id}, email: {self.email}, admin: {self.admin})'

class Habits(Base_users):
    __tablename__ = 'habits'
    id = Column(Integer, primary_key = True)
    habit_name = Column(Text)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)
    users = relationship("UserHabitAssociations", back_populates="habits")
    # users = relationship('UserHabitDays', backref='habits_ref', lazy=True)
    user_days = relationship('UserHabitDays', backref='user_days_ref', lazy=True)

    def __repr__(self):
        return f'Habits(id: {self.id}, habit_name: {self.habit_name})'

class UserHabitDays(Base_users):
    __tablename__ = 'user_habit_days'
    id = Column(Integer, primary_key = True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'UserHabitDays(id: {self.id}, habit_id: {self.habit_id}, user_id: {self.user_id}, ' \
            f'date: {self.date})'

# class HabitsRecorded(Base_users):
#     __tablename__ = 'habits_recorded'
#     id = Column(Integer, primary_key = True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     habit_name = Column(Text)
#     time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

class UserHabitAssociations(Base_users):
    __tablename__= 'user_habit_association'
    users_table_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    habits_table_id = Column(Integer, ForeignKey('habits.id'), primary_key=True)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)
    habits = relationship("Habits", back_populates="users")
    users = relationship("Users", back_populates="habits")

    def __repr__(self):
        return f'UserHabitAssociations(users_table_id: {self.users_table_id}, habits_table_id: {self.habits_table_id})' 

class BlogPosts(Base_users):
    __tablename__ = 'blog_posts'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(Text)
    description = Column(Text)
    date_published = Column(DateTime, nullable=False, default=datetime.now)
    edited = Column(Text)
    post_dir_name = Column(Text)
    word_doc_to_html_filename = Column(Text)
    images_dir_name = Column(Text)
    notes = Column(Text)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)


    def __repr__(self):
        return f'BlogPosts(id: {self.id}, user_id: {self.user_id}, title: {self.title})'

