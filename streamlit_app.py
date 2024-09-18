import streamlit as st


admin_username = "Dave"
admin_password = "p1"


users = {"Dave": "p1"}


def check_login(username, password):
    return username == admin_username and password == admin_password


def add_user(new_username, new_password):
    if new_username in users:
        st.error(f"User {new_username} already exists.")
    else:
        users[new_username] = new_password
        st.success(f"User {new_username} added successfully.")


def remove_user(username):
    if username in users:
        del users[username]
        st.success(f"User {username} removed successfully.")
    else:
        st.error(f"User {username} does not exist.")


st.title("User Management System")
st.subheader("Admin Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if check_login(username, password):
        st.success("Logged in successfully!")

        
        st.subheader("Add or Remove Users")

       
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")

        if st.button("Add User"):
            add_user(new_username, new_password)

     
        remove_username = st.text_input("Remove Username")

        if st.button("Remove User"):
            remove_user(remove_username)

     
        st.subheader("Current Users:")
        st.write(users)

    else:
        st.error("Invalid login credentials.")
