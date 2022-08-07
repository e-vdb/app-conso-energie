from passlib.hash import pbkdf2_sha256
import streamlit as st
import pandas as pd
from user_db import UserDatabase



class StreamlitAuthenticator:
    def __init__(self, df_credentials: pd.DataFrame):
        self.df_users = df_credentials
        self.allowed_users = self.df_users['username'].tolist()

    def authentication(self, main_app_fct_to_show):
        with st.sidebar.form("Connexion", clear_on_submit=True):
            username = st.text_input(label="Entrez votre nom")
            password = st.text_input(label="Entrez votre mot de passe", type="password")
            if st.form_submit_button("Se connecter"):
                if username in self.allowed_users:

                    hashed_password = self.df_users.loc[self.df_users['username'] == username]["password"].values[0]
                    if pbkdf2_sha256.verify(password, hashed_password):
                        st.success("Vous êtes correctement connecté.")
                        if 'name' not in st.session_state:
                                st.session_state['name'] = username
                    else:
                        st.error("Mauvais mot de passe.")
                else:
                    st.error("Cet utilisateur n'est pas autorisé à accéder à l'application.")

        if 'name' in st.session_state:
            main_app_fct_to_show()
        else:
            st.info("Connectez-vous pour accéder à l'application.")
