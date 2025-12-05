import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

def execute_query(query):
    connection = get_connection()
    try:
        df = pd.read_sql(query, connection)
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        connection.close()
    
    return df


if __name__ == "__main__":
    try:
        test_query = "SELECT * FROM customers LIMIT 5"
        df = execute_query(test_query)
        print(df)
    except Exception as e:
        print(f"Error: {e}")
