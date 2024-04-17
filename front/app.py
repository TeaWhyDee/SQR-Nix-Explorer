import streamlit as st

def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        # Check if username and password are correct (for demonstration purposes)
        if username == "admin" and password == "password":
            return True
        else:
            st.error("Invalid username or password")
            return False

def homepage():
    st.title("Welcome to My App")
    st.write("This is the homepage.")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Login", "Homepage"])

    if page == "Login":
        if login():
            st.experimental_rerun()
    elif page == "Homepage":
        homepage()

if __name__ == "__main__":
    main()
