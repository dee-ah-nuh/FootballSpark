import sqlite3
import os
import pandas as pd

def insert_dataframe_to_table(db_path, df, table_name):
    """
    Inserts a pandas DataFrame into the specified SQLite table.
    """
    conn = sqlite3.connect(db_path)
    try:
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Inserted {len(df)} rows into {table_name}.")
    except Exception as e:
        print(f"Error inserting into {table_name}: {e}")
    finally:
        conn.close()
