import mysql.connector
from config import DB_PASSWORD 
def func_real_db():
    real_db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = DB_PASSWORD,
        database = "real_db")
    return real_db

