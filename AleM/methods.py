import hashlib
import sqlite3
from database import conn  # Import the shared database connection

def _hash_password(password: str) -> str:
    """Hashes a password using SHA256. Private to this module."""
    return hashlib.sha256(password.encode()).hexdigest()

class DbUser:
    """A class to manage user-related database operations."""

    def create_user(self, username: str, password: str) -> bool:
        
        if not username or not password:
            return False

        hashed_pswd = _hash_password(password)
        
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, hashed_pswd) VALUES (?, ?)",
                    (username, hashed_pswd)
                )
                conn.commit()
            return True
        except (Exception, sqlite3.IntegrityError) as error:
            print(str(error))
            # This error occurs if the username is not unique.
            return False

    def check_auth(self, username: str, password: str) -> bool:
        """
        Verifies if a user exists and if the password is correct.

        Args:
            username: The username to check.
            password: The password to verify.

        Returns:
            True if the credentials are valid, otherwise False.
        """
        if not username or not password:
            return False

        hashed_pswd = _hash_password(password)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT hashed_pswd FROM users WHERE username = ?", (username,)
        )
        record = cursor.fetchone()
        conn.commit()
        return bool(record and record[0] == hashed_pswd)

    def get_user(self, username: str) -> dict | None:
        """
        Retrieves a user's data from the database.

        Args:
            username: The username of the user to retrieve.

        Returns:
            A dictionary with user data (id, username) if found, otherwise None.
        """
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username FROM users WHERE username = ?", (username,)
        )
        record = cursor.fetchone()
        if not record:
            return {"error": "utente non trovato"}
        
        if record:
            return {"id": record[0], "username": record[1]}
        return None

if __name__ == '__main__':
    # This block is for testing purposes.
    # It requires a 'database.py' with a 'create_table' function.
    print("Running tests for methods.py...")
    
    # In a real run, table creation should happen at app startup.
    from database import create_table
    create_table()
    
    db_user_manager = DbUser()
    
    # Test user creation
    print("Test create_user 'testuser1':", db_user_manager.create_user("testuser1", "password123"))
    print("Test create_user 'testuser1' again (should fail):", db_user_manager.create_user("testuser1", "password123"))
    print("Test create_user with empty credentials (should fail):", db_user_manager.create_user("", ""))
    
    # Test authentication
    print("Test check_auth 'testuser1' correct pass:", db_user_manager.check_auth("testuser1", "password123"))
    print("Test check_auth 'testuser1' wrong pass:", db_user_manager.check_auth("testuser1", "wrongpass"))
    print("Test check_auth 'nonexistentuser':", db_user_manager.check_auth("nonexistentuser", "somepass"))

    # Test retrieving a user
    user_data = db_user_manager.get_user("testuser1")
    print("Test get_user 'testuser1':", user_data)
    
    non_user_data = db_user_manager.get_user("nonexistentuser")
    print("Test get_user 'nonexistentuser':", non_user_data)

    print("Tests finished.")