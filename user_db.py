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

    def read_table(self):
        users = self.session.query(User)
        for user in users:
            print(user.username)
            print(user.mail)
            print(user.created_at)
            print(user.location)

    def return_table_as_df(self) -> pd.DataFrame:
        """
        Load the users-app table in a panda dataframe.
        Returns
        -------
        df: pd.Dataframe
        """
        df = pd.read_sql_query('select * from "users_app"', con=self.db)
        return df
