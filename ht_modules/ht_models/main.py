print("- in modelsMain")
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import relationship, backref, sessionmaker
# from .Base import Base_users, Base_cage, Base_bls, sess_users, sess_cage, sess_bls, \
#     engine_users, engine_cage, engine_bls
from .Base import dict_base, dict_engine, dict_sess

from .modelsUsers import Users, BlogPosts
# from .modelsCage import CageCompanies
# from .modelsBls import IndustryNames, IndustryValues, \
#     CommodityNames, CommodityValues
import os
from flask_login import LoginManager

sess_users = dict_sess['sess_users']

login_manager= LoginManager()
login_manager.login_view = 'bp_users.login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(any_name_for_id_obj):# any_name_for_id_obj can be any name because its an arg that is the user id.
    # This is probably created somewhere inside flask_login when the user gets logged in. But i've not been able to track it.
    return sess_users.query(Users).filter_by(id = any_name_for_id_obj).first()

