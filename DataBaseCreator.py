import sqlite3

if __name__ == '__main__':

    try:
        connection = sqlite3.connect('Healthapp.db')
        cursor = connection.cursor()
    except sqlite3.Error as error:
        print('Error while creating DataBase', error)
    finally:
        if connection:
            try:
                cursor.execute('CREATE TABLE users \
                (username VARCHAR(20) PRIMARY KEY NOT NULL,\
                 name VARCHAR(20) NOT NULL,\
                 last VARCHAR(20) NOT NULL,\
                 email VARCHAR(30) NOT NULL,\
                 password VARCHAR (30) NOT NULL);')

                print('Successfully crated users table')

                cursor.execute('CREATE TABLE consumption \
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,\
                 username VARCHAR(20) NOT NULL,\
                 foodname VARCHAR(20) NOT NULL,\
                 calories INT NOT NULL,\
                 date DATETIME DEFAULT CURRENT_TIMESTAMP);')

                print('Successfully created consumption table')

                connection.commit()
                cursor.close()
                connection.close()

            except sqlite3.Error as error:
                print('Error while creating tables:', error)
                cursor.close()
                connection.close()
