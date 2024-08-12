from db_config import load_config
from mysql.connector import connect, Error


def db_connect(config):
    """Connect to the PostgreSQL database server"""
    try:
        # connecting to the PostgreSQL server
        conn = connect(**config)
        print("[INFO] Conectado ao banco de dados MYSQL.")
        return conn
    except Error as error:
        print("[ERRO]", error)


if __name__ == "__main__":
    config = load_config()
    db_connect(config)
