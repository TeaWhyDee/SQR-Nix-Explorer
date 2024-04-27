import streamlit as st
from services.nix_api import NixAPI


async def search(api: NixAPI):
    store = st.selectbox("Store", await api.stores())
    packages = await api.packages(store)

    search_term = st.text_input("Search Packages", "")
    filtered_packages = [
        package for package in packages if search_term.lower() in package.lower()
    ]

    for package in filtered_packages:
        with st.container():
            col1, col2 = st.columns(2)

            closure_size = await api.closure_size(store, package)

            col1.write(f"**Name:** {package}")
            col1.write(f"**Closure Size:** {closure_size} packages")

            if col2.button(f"Delete {package}"):
                try:
                    await api.rm_package(package)
                    st.rerun()

                except Exception as e:
                    st.error(f"Error deleting package: {e}")

            st.markdown("---")

    if not filtered_packages:
        if st.button("Add Package"):
            if search_term:
                try:
                    await api.add_package(search_term)
                    st.success(f"Package '{search_term}' added successfully!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Error adding package: {e}")
