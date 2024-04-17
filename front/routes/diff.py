import streamlit as st

from services.nix_api import NixAPI

def diff(api: NixAPI):
    st.title("Difference between closures/paths")
    col1, col2, col3 = st.columns([2, 1, 2])
    col2.text('')
    col2.text('')
    
    packages = api.packages()
    
    selected_option1 = col1.selectbox("Package 1", map(lambda x: x.name, packages))
    submit_button = col2.button("Submit", use_container_width=True)
    selected_option2 = col3.selectbox("Package 2", map(lambda x: x.name, packages))

    if submit_button:
        closures = api.difference_closures(selected_option1, selected_option2 )
        paths = api.difference_paths(selected_option1, selected_option2 )
        data_col1, data_col2 = st.columns([1, 1])

        data_col1.write("Retrieved Closures:")
        data_col2.write("Retrieved Paths:")
        for item in closures:
            data_col1.write("- " + item)
        for item in paths:
            data_col2.write("- " + item)