import sqlite3
import csv

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS new_table (
            obs INTEGER,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            date INTEGER,
            latitude REAL,
            longitude REAL,
            zon_winds REAL,
            mer_winds REAL,
            humidity REAL,
            air REAL,
            temp REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Account (
            userId INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            password TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE,
            alerts TINYINT(1) NOT NULL,
            dateCreated DATE NOT NULL,
            isAdmin TINYINT(1) NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Alerts (
            userId INT NOT NULL,
            zone INT NOT NULL,
            email TINYINT(1) NOT NULL,
            text TINYINT(1) NOT NULL,
            FOREIGN KEY (userId) REFERENCES Account(userId)
        )
    ''')

    cursor.execute('''
        INSERT INTO Account (password, alerts, email, phone, dateCreated, isAdmin) 
        VALUES ('password123', 1, 'test@test.com', '13064443333', '2024-03-02', 0)
    ''')

    cursor.execute('''
        INSERT INTO Account (password, alerts, email, phone, dateCreated, isAdmin) 
        VALUES ('password1234', 1, 'test2@test2.com', '13064442222','2024-03-04', 1)
    ''')

    cursor.execute('''
        INSERT INTO Alerts (userId, zone, email, text) 
        VALUES ((SELECT userId FROM Account WHERE password = 'password123'), 2, 1, 0)
    ''')

    conn.commit()

def import_csv_to_table(conn, csv_file_path):
    cursor = conn.cursor()

    try:
        with open(csv_file_path, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            # Skip the header row
            next(csv_reader, None)

            # Insert data into the table
            for row in csv_reader:
                cursor.execute('''
                    INSERT INTO new_table
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', row)
                
        conn.commit()
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except Exception as e:
        print(f"Error: {e}")
        
def main():
    # Connect to SQLite in-memory database
    conn = sqlite3.connect(':memory:')

    # Specify the path to CSV file
    csv_file_path = 'code/data/cleaned_data.csv'

    # Create the table
    create_table(conn)

    # Import data from CSV to the table
    import_csv_to_table(conn, csv_file_path)

    # Query and print data from the table
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM new_table')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
