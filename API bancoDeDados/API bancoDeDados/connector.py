import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do arquivo .env

def get_connection():
    print("Tentando conectar ao banco de dados...")
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def close(self):
    if self.conn:
        self.conn.close()

