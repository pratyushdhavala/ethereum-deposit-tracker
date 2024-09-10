import psycopg2

def connect_to_db():
    try:

        connection = psycopg2.connect(
            host="localhost",
            database="ethereum",
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )


        cursor = connection.cursor()
        print("Connection to PostgreSQL established successfully.")
        return connection, cursor

    except Exception as error:
        print(f"Error connecting to PostgreSQL: {error}")
        return None, None


def close_db_connection(connection, cursor):
    try:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("PostgreSQL connection is closed.")
    except Exception as error:
        print(f"Error closing PostgreSQL connection: {error}")