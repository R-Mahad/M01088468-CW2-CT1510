import bcrypt
import os

# Path to the user data file used for registration & login
USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password):
    """
    Hashes a password using bcrypt with automatic salt generation.

    Args:
        plain_text_password (str): The plaintext password to hash.

    Returns:
        str: The hashed password as a UTF-8 string.
    """
    # Encode the password string into bytes (bcrypt works with bytes, not str)
    password_bytes = plain_text_password.encode("utf-8")

    # Generate a cryptographically secure salt using bcrypt
    salt = bcrypt.gensalt()

    # Hash the password bytes with the generated salt
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)

    # Decode the resulting hash back to a UTF-8 string so we can store it in a text file
    hashed_str = hashed_bytes.decode("utf-8")

    # Return the final hash string
    return hashed_str


def verify_password(plain_text_password, hashed_password):
    """
    Verifies a plaintext password against a stored bcrypt hash.

    Args:
        plain_text_password (str): The password to verify.
        hashed_password (str): The stored hash to check against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    # Encode both the plaintext password and the stored hash into bytes
    password_bytes = plain_text_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")

    # bcrypt.checkpw() automatically extracts the salt from the stored hash
    # and compares the hash of the input password with the stored one
    is_valid = bcrypt.checkpw(password_bytes, hashed_bytes)

    return is_valid

# TEMPORARY TEST CODE - Remove after testing
if __name__ == "__main__":
    test_password = "SecurePassword123"

    # Test hashing
    hashed = hash_password(test_password)
    print(f"Original password: {test_password}")
    print(f"Hashed password: {hashed}")
    print(f"Hash length: {len(hashed)} characters")

    # Test verification with correct password
    is_valid = verify_password(test_password, hashed)
    print(f"\nVerification with correct password: {is_valid}")

    # Test verification with incorrect password
    is_invalid = verify_password("WrongPassword", hashed)
    print(f"Verification with incorrect password: {is_invalid}")

def register_user(username, password):
    """
    Registers a new user by hashing their password and storing credentials.

    Args:
        username (str): The username for the new account.
        password (str): The plaintext password to hash and store.

    Returns:
        bool: True if registration successful, False if username already exists.
    """
    # 1. Check if the username already exists
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    # 2. Hash the user's password using bcrypt
    hashed_password = hash_password(password)

    # 3. Append the new user credentials to the file in "username,hashed_password" format
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed_password}\n")

    # 4. Confirm registration to the user
    print(f"Success: User '{username}' registered successfully!")
    return True

def user_exists(username):
    """
    Checks if a username already exists in the user database.

    Args:
        username (str): The username to check.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    # Handle the case where the file doesn't exist yet (no users registered)
    if not os.path.exists(USER_DATA_FILE):
        return False

    # Open the user data file and scan each line for the given username
    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            # Each line should be "username,hashed_password"
            stored_username, _ = line.strip().split(",", 1)

            # If the stored username matches the one we are checking, the user exists
            if stored_username == username:
                return True

    # If we finish the loop with no match, the user does not exist
    return False

def register_user(username, password):
    """
    Registers a new user by hashing their password and storing credentials.
    """
    # 1) Check if username already exists
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    # 2) Hash the password
    hashed_password = hash_password(password)

    # 3) Append new user credentials to the file
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed_password}\n")

    # 4) Tell the user it worked
    print(f"Success: User '{username}' registered successfully!")
    return True


def login_user(username, password):
    """
    Authenticates a user by verifying their username and password.

    Args:
        username (str): The username to authenticate.
        password (str): The plaintext password to verify.

    Returns:
        bool: True if authentication successful, False otherwise.
    """
    # Handle the case where no users are registered yet
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users are registered yet.")
        return False

    # Open the user data file and search for the username
    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            # Each line is "username,hashed_password"
            stored_username, stored_hash = line.strip().split(",", 1)

            if stored_username == username:
                # Username found → verify the password using bcrypt
                if verify_password(password, stored_hash):
                    print(f"Success: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False

    # If we reach here, the username was not found in the file
    print("Error: Username not found.")
    return False

def validate_username(username):
    """
    Validates username format.

    Returns: (is_valid, error_message)
    """
    # 1) Check length
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 characters long."

    # 2) Only allow letters and numbers
    if not username.isalnum():
        return False, "Username may only contain letters and numbers (no spaces or symbols)."

    # 3) If all good
    return True, ""


def validate_password(password):
    """
    Validates password strength.

    Args:
        password (str): The password to validate.

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    # Rule 1: Minimum and maximum length
    if len(password) < 6 or len(password) > 50:
        return False, "Password must be between 6 and 50 characters long."

    # (Optional) You could add more rules here:
    # - At least one digit
    # - At least one uppercase / lowercase letter
    # - At least one special character
    # But the lab only strictly specifies length, so we keep it simple.

    return True, ""

def display_menu():
    """Displays the main menu options."""
    print("\n" + "=" * 50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("=" * 50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-" * 50)


def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Register the user
            register_user(username, password)

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                # In a real application, you'd now access the domain features

                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()

1