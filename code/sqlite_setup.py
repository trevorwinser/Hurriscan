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
            userId INTEGER PRIMARY KEY AUTOINCREMENT,
            password TEXT NOT NULL,
            alerts BOOLEAN NOT NULL,
            dateCreated DATE NOT NULL,
            isAdmin BOOLEAN NOT NULL,
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Alerts (
            userId INTEGER NOT NULL,
            zone INTEGER NOT NULL,
            email BOOLEAN NOT NULL,
            text BOOLEAN NOT NULL,
            FOREIGN KEY (userId) REFERENCES Account(userId)
        )
    ''')

    cursor.execute('''
        INSERT INTO Account (password, alerts, dateCreated, isAdmin) 
        VALUES ('password123', 1, '2024-03-02', 0)
    ''')

    cursor.execute('''
        INSERT INTO Alerts (userId, zone, email, text) 
        VALUES ((SELECT userId FROM Account WHERE password = '123'), 2, 1, 0)
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
    csv_file_path = '/Users/julie/Downloads/cleaned_data.csv'

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
