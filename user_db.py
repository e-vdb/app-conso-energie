from sqlalchemy import Column, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.hash import pbkdf2_sha256
from datetime import datetime

import pandas as pd


base = declarative_base()


class User(base):
    __tablename__ = 'users_app'

    username = Column(String, primary_key=True)
    location = Column(String)
    mail = Column(String)
    password = Column(String)
    created_at = Column(Date)


class UserDatabase:
    def __init__(self, db):
        self.db = db
        Session = sessionmaker(self.db)
        self.session = Session()

    def add_user(self, name, location, email, password):
        new_user = User(username=name, location=location, mail=email, password=pbkdf2_sha256.hash(password),
                        created_at=datetime.now())
        self.session.add(new_user)
        self.session.commit()

    def return_table_as_df(self) -> pd.DataFrame:
        """
        Load the users-app table in a panda dataframe.
        Returns
        -------
        df: pd.Dataframe
        """
        df_users = pd.DataFrame(columns=['username', 'password', 'mail', 'created_at', 'location'])
        users = self.session.query(User)
        for count, user in enumerate(users):
            df_users.loc[count, 'username'] = user.username
            df_users.loc[count, 'password'] = user.password
            df_users.loc[count, 'location'] = user.location
            df_users.loc[count, 'created_at'] = user.created_at
            df_users.loc[count, 'mail'] = user.mail
        return df_users
