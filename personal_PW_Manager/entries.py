import mysql.connector
from cryptography.fernet import Fernet
import bcrypt

from database import DEFAULT_CONNECTION
from master_user import login_user


TestUser = ['user', '123123']


def get_master_key(username):
    try:
        cursor = DEFAULT_CONNECTION.cursor()
        get_key_query = '''
            SELECT master_key FROM Users WHERE username = %s;
        '''
        cursor.execute(get_key_query, (username,))
        user_data = cursor.fetchone()
        if user_data:
            return user_data[0]
        else:
            print("User '{}' does not exist.".format(username))
            return None
    except mysql.connector.Error as error:
        print("Error retrieving Master key: {}".format(error))
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

def encrypt_password(master_key, password):
    cipher_suite = Fernet(master_key.encode())
    return cipher_suite.encrypt(password.encode()).decode()

def entry_exists(cursor, user_id, website, website_username):
    check_entry_query = '''
        SELECT COUNT(*) FROM Entries
        WHERE user_id = %s AND website = %s AND website_username = %s;
    '''
    cursor.execute(check_entry_query, (user_id, website, website_username))
    count = cursor.fetchone()[0]
    return count > 0

def add_entry(username, website, website_username, website_password):
    try:
        cursor = DEFAULT_CONNECTION.cursor()
        user_id_query = '''
            SELECT user_id FROM Users WHERE username = %s;
        '''
        cursor.execute(user_id_query, (username,))
        user_id = cursor.fetchone()[0]
        
        if entry_exists(cursor, user_id, website, website_username):
            choice = input("An entry for this website/username combination already exists. Do you want to update it? (Y/N): ").lower()
            if choice == 'y':
                update_entry_query = '''
                    UPDATE Entries
                    SET encrypted_username_password = %s
                    WHERE user_id = %s AND website = %s AND website_username = %s;
                '''
                master_key = get_master_key(username)
                website_password = input('Enter your new password: ')
                confirm_website_password = input('Please Confirm your password: ')
                if website_password == confirm_website_password:

                    encrypted_password = encrypt_password(master_key, website_password)
                    cursor.execute(update_entry_query, (encrypted_password, user_id, website, website_username))
                    DEFAULT_CONNECTION.commit()
                    print("Entry for '{}' updated successfully.".format(website))
                    return
                else: 
                    print('Passwords do not match')
            else:
                print("No changes were made.")
                return

        master_key = get_master_key(username)
        if master_key:
            encrypted_password = encrypt_password(master_key, website_password)
            insert_entry_query = '''
                INSERT INTO Entries (user_id, website, website_username, encrypted_username_password)
                VALUES (%s, %s, %s, %s);
            '''
            cursor.execute(insert_entry_query, (user_id, website, website_username, encrypted_password))
            DEFAULT_CONNECTION.commit()
            print("Entry added successfully for user '{}'.".format(username))
    except mysql.connector.Error as error:
        print("Error adding entry: {}".format(error))
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

def get_entries(username):
    try:
        cursor = DEFAULT_CONNECTION.cursor()
        get_entries_query = '''
            SELECT website, website_username, encrypted_username_password FROM Entries
            WHERE user_id = (SELECT user_id FROM Users WHERE username = %s);
        '''
        cursor.execute(get_entries_query, (username,))
        entries = cursor.fetchall()
        if entries:
            return entries
        else:
            print("No entries found for user '{}'.".format(username))
            return []
    except mysql.connector.Error as error:
        print("Error retrieving entries: {}".format(error))
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

def delete_entry(username, website):
    try:
        cursor = DEFAULT_CONNECTION.cursor()
        delete_entry_query = '''
            DELETE FROM Entries
            WHERE user_id = (SELECT user_id FROM Users WHERE username = %s)
            AND website = %s;
        '''
        cursor.execute(delete_entry_query, (username, website))
        DEFAULT_CONNECTION.commit()
        if cursor.rowcount > 0:
            print("Entry for '{}' deleted successfully.".format(website))
        else:
            print("Entry for '{}' not found.".format(website))
    except mysql.connector.Error as error:
        print("Error deleting entry: {}".format(error))
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

def decrypt_password(username, website, website_username):
    try:
        cursor = DEFAULT_CONNECTION.cursor()
        get_encrypted_password_query = '''
            SELECT encrypted_username_password FROM Entries
            WHERE user_id = (SELECT user_id FROM Users WHERE username = %s)
            AND website = %s AND website_username = %s;
        '''
        cursor.execute(get_encrypted_password_query, (username, website, website_username))
        encrypted_password = cursor.fetchone()[0]
        
        fernet_key = get_master_key(username)
        cipher_suite = Fernet(fernet_key.encode())
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
        
        print(f"Decrypted password for {website}/{website_username}: {decrypted_password}")
    except mysql.connector.Error as error:
        print("Error decrypting password: {}".format(error))
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

if login_user(TestUser[0], TestUser[1]):

    #print(get_master_key(TestUser[0]))
    #add_entry(TestUser[0], 'google.com',  'epicGoogleUsername', 'securepassword123$$')
    #print(get_entries(TestUser[0]))
    #delete_entry('user', 'google.com')
    decrypt_password(TestUser[0], 'google.com', 'epicGoogleUsername')
    pass

