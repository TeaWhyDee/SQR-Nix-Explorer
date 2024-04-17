import streamlit as st
from services.nix_api import NixAPI


def search(api: NixAPI):
    packages = api.packages()

    search_term = st.text_input("Search Packages", "")
    filtered_packages = [
        package for package in packages if search_term.lower() in package.name.lower()
    ]

    for package in filtered_packages:
        with st.container():
            col1, col2 = st.columns(2)

            col1.write(f"**Name:** {package.name}")
            col1.write(f"**Closure Size:** {package.closure_size} packages")

            if col2.button(f"Delete {package.name}"):
                try:
                    api.rm_package(package.id)
                    st.rerun()

                except Exception as e:
                    st.error(f"Error deleting package: {e}")

            st.markdown("---")
