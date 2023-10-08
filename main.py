import mysql.connector
from sqlalchemy import create_engine
import pandas as pd


def connect_to_db(host="localhost", user="root", db_name="beers"):
    try:
        conn = mysql.connector.connect(
            host=host, user=user, password="root", auth_plugin="mysql_native_password"
        )

        # Create the database if it doesn't exist
        create_database(conn, db_name)

        # Set the database to the created/found one
        conn.database = db_name

        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)  # Exit the program with an error code


def create_database(conn, db_name="beers"):
    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)


def populate_database_from_csv(host="localhost", user="root", db_name="beers"):
    """
    Populate the MySQL database with data from CSV files.
    """
    password = "root"
    # Define the connection string and create the engine
    conn_string = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
    engine = create_engine(conn_string)

    # Load datasets from CSV into DataFrame
    drinker = pd.read_csv("data/drinker.csv")
    # bar = pd.read_csv('data/bar.csv')
    # beer = pd.read_csv('data/beer.csv')
    frequents = pd.read_csv("data/frequents.csv")
    serves = pd.read_csv("data/serves.csv")

    # Store data from DataFrame into MySQL database using the engine
    drinker.to_sql("drinker", engine, if_exists="replace", index=False)
    # bar.to_sql('bar', engine, if_exists='replace', index=False)
    # beer.to_sql('beer', engine, if_exists='replace', index=False)
    frequents.to_sql("frequents", engine, if_exists="replace", index=False)
    serves.to_sql("serves", engine, if_exists="replace", index=False)


def execute_query(conn):
    """
    Execute the complex SQL: Find drinkers who frequent bars that serve Amstel more than 2 times a week.
    """
    cursor = conn.cursor()
    query = """
    SELECT d.name, SUM(f.times_a_week) AS times
    FROM drinker d INNER JOIN frequents f ON d.name = f.drinker INNER JOIN serves s on f.bar = s.bar
    WHERE s.beer = 'Amstel'
    GROUP BY d.name
    HAVING SUM(f.times_a_week) > 2
    ORDER BY times;
    """
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    connect = connect_to_db()
    create_database(connect)
    populate_database_from_csv()
    final_results = execute_query(connect)
    print(final_results)
    connect.close()
