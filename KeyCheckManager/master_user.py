import bcrypt
import mysql.connector
from cryptography.fernet import Fernet

connection = mysql.connector.connect(
            host = '0.0.0.0',
            user = 'root',
            passwd = 'kali',
            database = 'pw_manager')

def hash_password(password):
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password.decode()

def verify_password(entered_password, hashed_password):
    # Verify the entered password against the hashed password using bcrypt
    return bcrypt.checkpw(entered_password.encode(), hashed_password.encode())

def create_master_user(master_username, master_password):

    hashed_superpassword = hash_password(master_username[::-1] + master_password)
    master_key  = Fernet.generate_key()

    try:
        
        cursor = connection.cursor()

        # Insert the master user into the Users table
        insert_master_user = '''
            INSERT INTO Users (username, encrypted_superpassword, master_key)
            VALUES (%s, %s, %s);
        '''
        cursor.execute(insert_master_user, (master_username, hashed_superpassword, master_key))
        print("Master user created and added to the database successfully.")

        # Commit changes
        connection.commit()

    except mysql.connector.Error as error:
        print("Error creating master user: {}".format(error))

    finally:
        # Close cursor and connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def login_user(master_username, master_password):

    password = master_username[::-1] + master_password

    try:
        cursor = connection.cursor()

        # Fetch the hashed password for the entered username from the Users table
        get_hashed_password = '''
            SELECT encrypted_superpassword FROM Users WHERE username = %s;
        '''
        cursor.execute(get_hashed_password, (master_username,))
        user_data = cursor.fetchone()

        if user_data:

            hashed_password_from_db = user_data[0]

            # Verify the entered password against the hashed password
            if verify_password(password, hashed_password_from_db):
                LoggedIn = True
                print("Login successful! Welcome, {}.".format(master_username))


            else:
                LoggedIn = False
                print("Invalid password. Login failed.")
        else:
            print("User '{}' does not exist.".format(username))

    except mysql.connector.Error as error:
        print("Error while logging in: {}".format(error))
        
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        else:
            print('no master key found')

    return LoggedIn
    
def delete_user(master_username, master_password):

    if login_user(master_username, master_password):
        try:
            cursor = connection.cursor()
            delete_user_query = '''
                DELETE FROM Users WHERE username = %s;
            '''
            cursor.execute(delete_user_query, (username,))
            connection.commit()
            if cursor.rowcount > 0:
                print(f"User '{username}' deleted successfully.")
            else:
                print("User '{}' does not exist.".format(username))
        except mysql.connector.Error as error:
            print("Error deleting user: {}".format(error))
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
    else:
        print('Unnable to Loggin. No changes have been placed')

if __name__ == '__main__':
    username = input('Enter Username:')
    password = input('Enter Password: ')

    create_master_user(username, password)
    #login_user(username, password)
    #delete_user(username, password)

