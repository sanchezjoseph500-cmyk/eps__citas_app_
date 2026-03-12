import psycopg2
import psycopg2.extras
from config import Config

def get_connection():
    conexion = psycopg2.connect(Config.DATABASE_URL)
    return conexion
