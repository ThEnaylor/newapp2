import streamlit as st
import csv
import os

# Define the file to store user data
USER_DATA_FILE = "userlist.csv"

def load_users():
    """Load users from the CSV file."""
    users = {}
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    users[row[0]] = row[1]
    return users

def save_users(users):
    """Save users to the CSV file."""
    with open(USER_DATA_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        for username, password in users.items():
            writer.writerow([username, password])

# Load users into the session state
if 'users' not in st.session_state:
    st.session_state['users'] = load_users()

if 'admin_logged_in' not in st.session_state:
    st.session_state['admin_logged_in'] = False

def check_login(username, password):
    """Check if login credentials are correct."""
    return username in st.session_state['users'] and st.session_state['users'][username] == password

def add_user(new_username, new_password):
    """Add a new user."""
    if new_username in st.session_state['users']:
        st.error(f"User {new_username} already exists.")
    else:
        st.session_state['users'][new_username] = new_password
        save_users(st.session_state['users'])
        st.success(f"User {new_username} added successfully.")

def remove_user(username):
    """Remove an existing user."""
    if username in st.session_state['users']:
        del st.session_state['users'][username]
        save_users(st.session_state['users'])
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
        add_user(new_username, new_password)

    remove_username = st.text_input("Remove Username")

    if st.button("Remove User"):
        remove_user(remove_username)

    st.subheader("Current Users:")
    st.write(st.session_state['users'])

    if st.button("Logout"):
        st.session_state['admin_logged_in'] = False




    
    
