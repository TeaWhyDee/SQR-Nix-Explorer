from copy import deepcopy
import streamlit as st

from services.nix_api import NixAPI


async def diff_stores(api: NixAPI):
    st.title("Difference between stores")
    col1, col2, col3 = st.columns([2, 1, 2])
    col2.text("")
    col2.text("")

    stores1 = await api.stores()
    stores2 = deepcopy(stores1)

    store1 = col1.selectbox("Store 1", stores1)
    submit_button = col2.button("Submit", use_container_width=True)
    store2 = col3.selectbox("Store 2", stores2)

    if submit_button:
        paths = await api.difference_paths(store1, store2)
        data_col1, _ = st.columns([1, 1])

        for item in paths:
            data_col1.write("- " + item)
