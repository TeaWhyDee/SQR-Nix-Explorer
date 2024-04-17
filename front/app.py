import streamlit as st
from routes.diff import diff
from routes.search import search
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


def main():
    api = MockNixApi(StSessKvStore("mock-api-"))

    LOGIN = "Login"
    REGISTER = "Register"
    DIFF = "Diff"
    SEARCH = "Search"

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to", [DIFF, SEARCH] if api.is_logged_in() else [LOGIN, REGISTER]
    )

    if page == LOGIN:
        if login(api):
            st.rerun()
    elif page == REGISTER:
        if register(api):
            st.rerun()
    elif page == DIFF:
        if diff(api):
            st.rerun()
    elif page == SEARCH:
        if search(api):
            st.rerun()
    else:
        st.error("Invalid page!")


if __name__ == "__main__":
    main()
