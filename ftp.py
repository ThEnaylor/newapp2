from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def start_ftp_server():
    # Create an authorizer object that manages authentication
    authorizer = DummyAuthorizer()

    # Add user permissions: username, password, directory, permissions
    # Permissions: "elradfmw" (read/write permissions)
    # Change "user" and "password" to your preferred credentials
    authorizer.add_user("user", "password", "ftp_files", perm="elradfmw")

    # Add an anonymous user with read-only permissions (optional)
    # authorizer.add_anonymous("/path/to/ftp/directory", perm="elr")

    # Create an FTP handler with the authorizer
    handler = FTPHandler
    handler.authorizer = authorizer

    # Create and configure the FTP server
    address = ('0.0.0.0', 21)  # 0.0.0.0 binds to all available interfaces
    server = FTPServer(address, handler)

    # Start the FTP server
    print("FTP server is running on port 21...")
    server.serve_forever()

if __name__ == "__main__":
    start_ftp_server()
