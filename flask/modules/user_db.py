import sqlite3


def get_connection_db() -> sqlite3.Connection:
    """
    Establish a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.
    """
    connection = sqlite3.connect("users.db")
    connection.row_factory = sqlite3.Row
    return connection


def initialize_db() -> None:
    """
    Initialize the SQLite database by creating the 'users'
    table if it does not already exist.
    This function creates a table to store user information,
    including a unique username
    and password. If the table already exists,
    this operation will have no effect.
    """
    connection = get_connection_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """
    )
    connection.commit()
    connection.close()


def add_member(username: str, password: str) -> None:
    """
    Add a new user to the database.

    Parameters:
        username (str): The username for the new user. Must be unique.
        password (str): The password for the new user.

    Raises:
        ValueError: If the username already exists in the database.
    """
    connection = get_connection_db()
    cursor = connection.cursor()

    # Check if the username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        return

    # If the username does not exist, proceed to add the member
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )
        connection.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error: {str(e)}")
    finally:
        connection.close()


def check_user_credentials(username: str, password: str) -> sqlite3.Row:
    """
    Check if a user with the given username and password exists in the database.

    Parameters:
        username (str): The username of the user to check.
        password (str): The password of the user to check.

    Returns:
        sqlite3.Row: A row object containing user information if the credentials are valid,
                      or None if they are not found.
    """
    connection = get_connection_db()
    cursor = connection.cursor()

    # Check if the user exists with the given username and password
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", (username, password)
    )
    user = cursor.fetchone()

    connection.close()
    return user  # Returns None if not found, or a row object if found
