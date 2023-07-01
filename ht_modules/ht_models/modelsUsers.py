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
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

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

        return sess.query(Users).get(user_id)

    def __repr__(self):
        return f'Users(id: {self.id}, email: {self.email}, admin: {self.admin})'


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
# if 'users' in inspect(engine).get_table_names():
#     print("db already exists")
# else:

#     Base.metadata.create_all(engine)
#     print("NEW db created.")