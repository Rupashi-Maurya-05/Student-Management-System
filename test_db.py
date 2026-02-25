from db_conn import create_connection

conn = create_connection()
if conn:
    print(" Connection Successful!")
    conn.close()
else:
    print(" Connection Failed!")
