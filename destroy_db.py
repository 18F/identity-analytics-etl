import src


def destroy():
    db_conn = src.DataBaseConnection()
    db_conn.drop_tables()
    db_conn.close_connection()

if __name__ == '__main__':
    destroy()
