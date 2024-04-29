import streamlit as st
from services.nix_api import NixAPI


async def stores(api: NixAPI):
    stores = await api.stores()

    search_term = st.text_input("Search Stores", "")
    filtered_stores = [
        store for store in stores if search_term.lower() in store.lower()
    ]

    for store in filtered_stores:
        with st.container():
            col1, col2 = st.columns(2)

            col1.write(f"**{store}**")

            if col2.button("Delete"):
                try:
                    await api.rm_store(store)
                    st.rerun()

                except Exception as e:
                    st.error(f"Error deleting store: {e}")

            st.markdown("---")

    if not filtered_stores:
        if st.button("Add Store"):
            if search_term:
                try:
                    await api.add_store(search_term)
                    st.success(f"Store '{search_term}' added successfully!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Error adding store: {e}")
