from database_connection import DataBaseConnection


def destroy():
    db_conn = DataBaseConnection()
    db_conn.drop_tables()
    db_conn.close_connection()

if __name__ == '__main__':
    destroy()
