import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


def conectar():
    host = os.getenv("DB_HOST") or "127.0.0.1"
    user = os.getenv("DB_USER") or "root"
    password = os.getenv("DB_PASSWORD") or ""
    database = os.getenv("DB_NAME") or "estudio_tatuagem"
    port = int(os.getenv("DB_PORT") or "3306")

    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        autocommit=False,
    )