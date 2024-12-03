import streamlit as st
import os

# Define the file to store user data
USER_DATA_FILE = "userlist.csv"

def load_users():
    """Load users from the CSV file."""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            lines = file.readlines()
        return {line.split(",")[0]: line.split(",")[1].strip() for line in lines if line.strip()}
    return {}

def save_user_append(new_username, new_password):
    """Append a single user to the CSV file."""
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{new_username},{new_password}\n")

# Load users into the session state
if 'users' not in st.session_state:
    st.session_state['users'] = load_users()

if 'admin_logged_in' not in st.session_state:
    st.session_state['admin_logged_in'] = False

def check_login(username, password):
    """Check if login credentials are correct."""
    return username in st.session_state['users'] and st.session_state['users'][username] == password

#def add_user(new_username, new_password):
#    """Add a new user."""
#    if new_username in st.session_state['users']:
#        st.error(f"User {new_username} already exists.")
#    else:
#        st.session_state['users'][new_username] = new_password
#        save_user_append(new_username, new_password)
#        st.success(f"User {new_username} added successfully.")

def remove_user(username):
    """Remove an existing user."""
    if username in st.session_state['users']:
        del st.session_state['users'][username]
        with open(USER_DATA_FILE, "w") as file:
            for username, password in st.session_state['users'].items():
                file.write(f"{username},{password}\n")
        st.success(f"User {username} removed successfully.")
    else:
        st.error(f"User {username} does not exist.")

# Streamlit UI
st.title("User Management System")

if not st.session_state['admin_logged_in']:
    st.subheader("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_login(username, password):
            st.session_state['admin_logged_in'] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid login credentials.")
else:
    st.subheader("Add or Remove Users")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Add User"):
        st.write("button press registered")
        with open("test.txt", "w") as yid:
            yid.write("workin")
            yid.close()
        with open(USER_DATA_FILE, "a") as file:
            file.write("Working,Working")

    remove_username = st.text_input("Remove Username")

    if st.button("Remove User"):
        remove_user(remove_username)

    if st.button("Logout"):
        st.session_state['admin_logged_in'] = False






    
    
