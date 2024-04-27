from copy import deepcopy
import streamlit as st

from services.nix_api import NixAPI


async def diff_packages(api: NixAPI):
    st.title("Difference between packages")
    col1, col2, col3 = st.columns([2, 1, 2])
    col2.text("")
    col2.text("")

    stores1 = await api.stores()
    stores2 = deepcopy(stores1)

    store1 = col1.selectbox("Store 1", stores1)
    submit_button = col2.button("Submit", use_container_width=True)
    store2 = col3.selectbox("Store 2", stores2)

    packages1 = await api.packages(store1)
    packages2 = await api.packages(store2)

    package1 = col1.selectbox("Package 1", packages1)
    package2 = col3.selectbox("Package 2", packages2)

    if submit_button:
        paths = await api.difference_closures(store1, package1, store2, package2)
        data_col1, _ = st.columns([1, 1])

        for item in paths:
            data_col1.write("- " + item)
