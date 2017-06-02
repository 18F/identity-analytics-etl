from database_connection import DataBaseConnection
from queries import Queries

def main():
    db_conn = DataBaseConnection()
    db_conn.drop_tables()
    db_conn.close_connection()

if __name__ == '__main__':
    main()
