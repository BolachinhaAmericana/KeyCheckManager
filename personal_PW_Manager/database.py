import mysql.connector

def create_database():

    try:
        connection = mysql.connector.connect(
            host = '0.0.0.0',
            user = 'root',
            passwd = 'kali',
            database = 'pw_manager')
        
    except mysql.connector.errors.ProgrammingError:
        
        connection = mysql.connector.connect(
        host = '0.0.0.0',
        user = 'root',
        passwd = 'kali',)
        
    
        cursor = connection.cursor()
        cursor.execute('CREATE DATABASE pw_manager;')

        connection = mysql.connector.connect(
        host = '0.0.0.0',
        user = 'root',
        passwd = 'kali',
        database = 'pw_manager')

    try:
        # Create cursor
        cursor = connection.cursor()

        # Execute SQL statements for creating tables
        create_users_table = '''
        CREATE TABLE Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            encrypted_superpassword TEXT NOT NULL,
            master_key TEXT NOT NULL
        );
    '''

        cursor.execute(create_users_table)
        print("Users table created successfully.")

        create_entries_table = '''
            CREATE TABLE Entries (
                entry_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                website VARCHAR(100) NOT NULL,
                website_username VARCHAR(50) NOT NULL,
                encrypted_username_password TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            );
        '''
        cursor.execute(create_entries_table)
        print("Entries table created successfully.")

        # Commit changes
        connection.commit()


    except mysql.connector.Error as error:
        print("Error creating database tables: {}".format(error))

    finally:
        # Close cursor and connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

        return None

def reset_database():
    try:
        connection = mysql.connector.connect(
            host = '0.0.0.0',
            user = 'root',
            passwd = 'kali',
            database = 'pw_manager'
)
    except mysql.connector.errors.ProgrammingError:
        
        connection = mysql.connector.connect(
        host = '0.0.0.0',
        user = 'root',
        passwd = 'kali',)
    cursor = connection.cursor()

    db_name = 'pw_manager'
    cursor.execute(f'DROP DATABASE IF EXISTS {db_name}')
    print('Database Deleted')

    create_database()

DEFAULT_CONNECTION = mysql.connector.connect(
                        host = '0.0.0.0',
                        user = 'root',
                        password = 'kali',
                        database = 'pw_manager'
)

if __name__ == '__main__':
    #reset_database()
    #create_database()
    pass