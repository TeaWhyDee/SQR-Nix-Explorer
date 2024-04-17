import streamlit as st
from services.mock_nix_api import MockNixApi
from services.nix_api import NixAPI
from services.st_sess_kv_store import StSessKvStore

def login(api: NixAPI):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        try:
            api.login(username, password)
            return True
        except ValueError:
            st.error("Invalid username or password")
            return False

def register(api: NixAPI):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Register")

    if login_button:
        try:
            api.register(username, password)
            return True
        except ValueError:
            st.error("Invalid username or password")
            return False

def homepage():
    st.title("Welcome to My App")
    st.write("This is the homepage.")


def main():
    api = MockNixApi(StSessKvStore("mock-api-"))

    LOGIN = "Login"
    HOMEPAGE = "Homepage"
    REGISTER = "Register"

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", [HOMEPAGE] if api.is_logged_in() else [LOGIN, REGISTER])

    if page == LOGIN:
        if login(api):
            st.rerun()
    elif page == HOMEPAGE:
            homepage()
    elif page == REGISTER:
        if register(api):
            st.rerun()
    else:
        st.error("Invalid page!")


if __name__ == "__main__":
    main()
