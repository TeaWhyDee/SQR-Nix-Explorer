import asyncio
import os
import streamlit as st
from routes.dif_packages import diff_packages
from routes.diff_stores import diff_stores
from routes.search import search
from routes.stores import stores
from services.mock_nix_api import MockNixApi
from services.nix_api import NixAPI
from services.rest_nix_api import RestNixApi
from services.st_sess_kv_store import StSessKvStore


API = os.environ["NIX_EXPLORER_API"]  # mock or a url like https://sqr.teawide.xyz/


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
    api = (
        MockNixApi(StSessKvStore("mock-api-"))
        if API == "mock"
        else RestNixApi(API, StSessKvStore("rest-api-"))
    )

    LOGIN = "Login"
    REGISTER = "Register"
    STORES = "Manage Stores"
    SEARCH = "Manage Packages"
    DIFF_STORES = "Diff Stores"
    DIFF_PACKAGES = "Diff Packages"

    st.sidebar.title("Navigation")
    ili = await api.is_logged_in()
    page = st.sidebar.radio(
        "Go to",
        [STORES, SEARCH, DIFF_STORES, DIFF_PACKAGES] if ili else [LOGIN, REGISTER],
    )
    if ili:
        logout = st.sidebar.button(label="Logout")

        if logout:
            await api.logout()
            st.rerun()

    if page == LOGIN:
        logged_in = await login(api)
        if logged_in:
            st.rerun()
    elif page == REGISTER:
        registered = await register(api)
        if registered:
            st.rerun()
    elif page == SEARCH:
        await search(api)
    elif page == DIFF_STORES:
        await diff_stores(api)
    elif page == DIFF_PACKAGES:
        await diff_packages(api)
    elif page == STORES:
        await stores(api)
    else:
        st.error("Invalid page!")


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
