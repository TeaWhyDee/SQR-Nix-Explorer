import asyncio
import streamlit as st
from routes.diff_stores import diff_stores
from routes.search import search
from services.mock_nix_api import MockNixApi
from services.nix_api import NixAPI
from services.st_sess_kv_store import StSessKvStore


async def login(api: NixAPI):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        try:
            await api.login(username, password)
            return True
        except ValueError:
            st.error("Invalid username or password")
            return False


async def register(api: NixAPI):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Register")

    if login_button:
        try:
            await api.register(username, password)
            return True
        except ValueError:
            st.error("Invalid username or password")
            return False


async def main():
    api = MockNixApi(StSessKvStore("mock-api-"))

    LOGIN = "Login"
    REGISTER = "Register"
    SEARCH = "Search"
    DIFF_STORES = "Diff Stores"

    st.sidebar.title("Navigation")
    ili = await api.is_logged_in()
    page = st.sidebar.radio(
        "Go to", [SEARCH, DIFF_STORES] if ili else [LOGIN, REGISTER]
    )

    if page == LOGIN:
        logged_in = await login(api)
        if logged_in:
            st.experimental_rerun()
    elif page == REGISTER:
        registered = await register(api)
        if registered:
            st.experimental_rerun()
    elif page == SEARCH:
        await search(api)
    elif page == DIFF_STORES:
        await diff_stores(api)
    else:
        st.error("Invalid page!")


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
