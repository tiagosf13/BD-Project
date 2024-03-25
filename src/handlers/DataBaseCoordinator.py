import json, pyodbc
from handlers.Retrievers import get_current_dir


def read_json(filename):

    with open(get_current_dir() + filename, "r", encoding="utf8") as file:
        data = json.load(file)
    return data


def read_sql_file(filename):
    
    with open(get_current_dir() + filename, "r", encoding="utf8") as file:
        sql_query = file.read()
    return sql_query


def db_query(query, params=None):

    # For Laptop Development
    #credentials = read_json("/credentials/DataBaseCredentialsLaptop.json")

    # Get the credentials for accessing the database
    credentials = read_json("/credentials/DataBaseCredentials.json")

    # Connect to the database PSQL
    """ conn = psycopg2.connect(
        host=credentials["host"],
        dbname=credentials["dbname"],
        user=credentials["user"],
        password=credentials["password"],
        port=credentials["port"]
    ) """

    # Connect to the database SQL
    conn = pyodbc.connect(
        Driver='{SQL Server}',
        Server=credentials["host"],
        Database=credentials["dbname"]
    )

    # Initiate the cursor
    cur = conn.cursor()

    # Check if there is any parameters
    if params:

        # Execute query with parameters
        cur.execute(query, params)

    else:

        # Execute query without parameters
        cur.execute(query)

    # Define select_in_query as False by default
    select_in_query = False

    # Check if the query has SELECT
    if ("SELECT" in query or "OUTPUT" in query) and not "CREATE" in query:

        # Fetch all the data
        data = cur.fetchall()
        select_in_query = True

    # Commit the connection
    conn.commit()

    # Close the cursor
    cur.close()

    # Close the connection
    conn.close()

    # Check if the query has SELECT
    if select_in_query:

        # Return the requested data
        return data


def check_database_tables_exist():
    """
                    ---------------> users <------ emergency_codes
                    |                ^   ^
                    |                |    \
                    |                |     \
                    |                carts  \
                    |                |       \
                    |                |        \
                    |                v         \
                    orders ----> products <--- reviews
    """
    
    # Read the SQL files for creating the tables
    create_table_users = read_sql_file("/queries/create_users_table.sql")
    create_table_products = read_sql_file("/queries/create_products_table.sql")
    create_table_emergency_codes = read_sql_file("/queries/create_emergency_codes_table.sql")
    create_table_carts = read_sql_file("/queries/create_carts_table.sql")
    create_table_reviews = read_sql_file("/queries/create_reviews_table.sql")
    create_table_orders = read_sql_file("/queries/create_orders_table.sql")

    # Execute the SQL queries for creating the tables
    db_query(create_table_users)
    db_query(create_table_products)
    db_query(create_table_emergency_codes)
    db_query(create_table_carts)
    db_query(create_table_reviews)
    db_query(create_table_orders)