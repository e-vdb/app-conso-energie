"""
Authentication module.

Source:
https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso
"""

import streamlit as st


def check_password():
    """Return `True` if the user had a correct password."""

    def password_entered():
        """Check whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.sidebar.text_input(
            "Username", on_change=password_entered, key="username"
        )
        st.sidebar.text_input(
            "Password",
            type="password",
            on_change=password_entered,
            key="password",
        )
        return False
    if not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.sidebar.text_input(
            "Username", on_change=password_entered, key="username"
        )
        st.sidebar.text_input(
            "Password",
            type="password",
            on_change=password_entered,
            key="password",
        )
        st.sidebar.error("😕 User not known or password incorrect")
        return False

    # Password correct.

    return True
