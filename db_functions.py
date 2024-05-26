import os
import sqlite3
import sys

db_path = str
app_database = str

# Modify database path if .exe
if getattr(sys, "frozen", False):
    db_path = os.path.join(os.path.dirname(sys.executable), ".dbs")
    app_database = os.path.join(db_path, "app_db.db")   
elif __file__:
    db_path = os.path.join(os.path.dirname(__file__), ".dbs")
    app_database = os.path.join(db_path, "app_db.db")

# Create database and directory if not exists
def initialise_database():
    try:
        if not os.path.exists(db_path):
            create_database_dir(db_path)
        create_database_or_database_table("logs")
    except Exception as e:
        print(f"Initialise database error: {e}")

def create_database_dir(db_dir_path: str):
    try:
        if not os.path.exists(db_dir_path):
            os.makedirs(db_dir_path, exist_ok=True)
            print(f"Logs database directory created: {db_path}")
    except Exception as e:
        print(f"Create database directory error: {e}")

def create_database_or_database_table(table_name: str, database_location=app_database):
    try:
        connection = sqlite3.connect(database_location)
        cursor = connection.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (date TEXT, event TEXT, description TEXT)""")
        connection.commit()
        connection.close()
        print(f"Logs database created: {database_location}")
    except Exception as e:
        print(f"Create database error: {e}")
        connection.close()


def add_event_to_database_table(event_date: str, event: str, description: str, table: str, database=app_database):
    try:
        connection = sqlite3.connect(app_database)
        cursor = connection.cursor()
        cursor.execute(f"""INSERT INTO {table} VALUES (?, ?, ?)""", (event_date, event, description))
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Log event to datebase error: {e}")
        connection.close()

def delete_events_from_database_table(delete_date: str, table: str, database=app_database):
    try:
        connection = sqlite3.connect(app_database)
        cursor = connection.cursor()
        cursor.execute(f"""DELETE FROM {table} 
        WHERE date < ?""", (delete_date,))
        connection.commit()
        connection.close()
        print(f"Deleted logs prior to {delete_date}")
    except Exception as e:
        print(f"Delete events from database error: {e}")
        connection.close()

def write_logs_to_text(table: str, database=app_database):
    try:
        connection = sqlite3.connect(app_database)
        cursor = connection.cursor()
        cursor.execute(f"""SELECT * FROM {table}""")
        log_data = cursor.fetchall()

        if log_data:
            log_file = open("logs.txt", "w")
            log_file.write("Date".rjust(0))
            log_file.write("Event".rjust(5))
            log_file.write("Description".rjust(5))
            log_file.writelines("")

            for row in log_data:
                row = str(row)
                log_file.write("\n%s\n" % row)

            log_file.close()

        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Logs to text file error: {e}")
        connection.close()