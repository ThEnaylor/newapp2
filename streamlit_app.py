import streamlit as st
from ftplib import FTP
import os

# FTP Server Credentials
FTP_HOST = "86.27.255.20"
FTP_PORT = 21
FTP_USER = "user"
FTP_PASS = "password"

# FTP File for storing user data
USER_DATA_FILE = "userlist.csv"


def read_file_from_ftp(filename):
    """Reads a file from the FTP server."""
    with FTP() as ftp:
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)
        content = []
        try:
            ftp.retrlines(f"RETR {filename}", content.append)  # Retrieve the file
        except Exception as e:
            if "550" in str(e):  # File not found
                st.warning(f"File {filename} not found on server. Starting fresh.")
            else:
                raise e
        return content


def append_to_ftp_file(filename, new_content):
    """Appends new content to a file on the FTP server."""
    with FTP() as ftp:
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)

        # Retrieve existing content
        existing_content = []
        try:
            ftp.retrlines(f"RETR {filename}", existing_content.append)
        except Exception as e:
            if "550" in str(e):  # File not found on server
                existing_content = []  # Start fresh if file doesn't exist
            else:
                raise e

        # Combine the existing content with the new content
        updated_content = "\n".join(existing_content + [new_content])  # Ensure new content is on a new line

        # Write back the updated content to the file
        with open("tempfile.csv", "w") as temp_file:
            temp_file.write(updated_content)  # Ensure the file ends with a newline

        with open("tempfile.csv", "rb") as temp_file:
            ftp.storbinary(f"STOR {filename}", temp_file)

        os.remove("tempfile.csv")  # Cleanup temporary file



def load_users_from_ftp():
    """Load users from the CSV file on FTP server."""
    content = read_file_from_ftp(USER_DATA_FILE)
    return {line.split(",")[0]: line.split(",")[1].strip() for line in content if line.strip()}


def save_user_append_to_ftp(new_username, new_password):
    """Append a single user to the CSV file on FTP server."""
    new_content = f"{new_username},{new_password}\n"
    append_to_ftp_file(USER_DATA_FILE, new_content)


def remove_user_from_ftp(username):
    """Remove an existing user from the FTP file."""
    with FTP() as ftp:
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)

        # Retrieve existing content
        existing_content = []
        try:
            ftp.retrlines(f"RETR {USER_DATA_FILE}", existing_content.append)
        except Exception as e:
            if "550" in str(e):  # File not found
                st.error("User list not found on the server.")
                return
            else:
                raise e

        # Remove the specified user
        updated_content = "\n".join(
            [line for line in existing_content if not line.startswith(f"{username},")]
        )

        # Write back the updated content to the file
        with open("tempfile.csv", "w") as temp_file:
            temp_file.write(updated_content)

        with open("tempfile.csv", "rb") as temp_file:
            ftp.storbinary(f"STOR {USER_DATA_FILE}", temp_file)

        os.remove("tempfile.csv")  # Cleanup temporary file
        st.success(f"User {username} removed successfully.")


# Load users into the session state
if "users" not in st.session_state:
    st.session_state["users"] = load_users_from_ftp()

if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False


def check_login(username, password):
    """Check if login credentials are correct."""
    return username in st.session_state["users"] and st.session_state["users"][username] == password


# Streamlit UI
st.title("User Management System")

if not st.session_state["admin_logged_in"]:
    st.subheader("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_login(username, password):
            st.session_state["admin_logged_in"] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid login credentials.")
else:
    st.subheader("Add or Remove Users")

    # Add User
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Add User"):
        if new_username in st.session_state["users"]:
            st.error(f"User {new_username} already exists.")
        else:
            save_user_append_to_ftp(new_username, new_password)
            st.session_state["users"][new_username] = new_password
            st.success(f"User {new_username} added successfully.")

    # Remove User
    remove_username = st.text_input("Remove Username")
    if st.button("Remove User"):
        if remove_username in st.session_state["users"]:
            remove_user_from_ftp(remove_username)
            del st.session_state["users"][remove_username]
        else:
            st.error(f"User {remove_username} does not exist.")

    # Logout
    if st.button("Logout"):
        st.session_state["admin_logged_in"] = False
