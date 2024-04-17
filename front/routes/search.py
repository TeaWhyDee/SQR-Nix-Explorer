import streamlit as st
from services.nix_api import NixAPI


def search(api: NixAPI):
    packages = api.packages()

    search_term = st.text_input("Search Packages", "")
    filtered_packages = [
        package for package in packages if search_term.lower() in package.name.lower()
    ]

    for package in filtered_packages:
        st.write(f"- **Name:** {package.name}")
        st.write(f"- **Closure Size:** {package.closure_size} bytes")
        st.markdown("---")  # Separator