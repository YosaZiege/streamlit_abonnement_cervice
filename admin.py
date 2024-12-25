import psycopg2
from psycopg2 import sql

host = "localhost"  
port = 5432  
dbname = "streamlitdatabase"
user = "yosa"
password = "root"

try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    cursor = connection.cursor()
    
except Exception as error:
    print(f"Error: {error}")