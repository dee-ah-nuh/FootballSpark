import sqlite3
import os
import traceback

def get_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'football_data.db')
    return sqlite3.connect(db_path)

def execute_sql_files(sql_folder):
    conn = get_connection()
    cursor = conn.cursor()
    executed_files = []
    for filename in os.listdir(sql_folder):
        if filename.endswith('.sql'):
            file_path = os.path.join(sql_folder, filename)
            print(f"Executing {file_path}")
            try:
                with open(file_path, 'r') as f:
                    sql_script = f.read()
                cursor.executescript(sql_script)
                executed_files.append(file_path)
            except Exception as e:
                print(f"Error executing {file_path}: {e}")
                traceback.print_exc()
    conn.commit()
    conn.close()
    return executed_files

if __name__ == "__main__":
    sql_folder = os.path.dirname(__file__)
    executed_files = execute_sql_files(sql_folder)
    print("Executed all SQL files in the folder:")
    for path in executed_files:
        print(path)

    # Show all tables in the database
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in database:", [table[0] for table in tables])
    except Exception as e:
        print(f"Error fetching tables: {e}")
        traceback.print_exc()
    conn.close()
