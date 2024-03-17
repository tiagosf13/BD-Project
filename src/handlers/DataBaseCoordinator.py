import os, json, psycopg2, re
import pyodbc


def read_json(filename):


    if os.name == "nt":
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__)).split("\\handlers")[0]
    else:
        # Get the current working directory
        current_directory = os.path.dirname(os.path.abspath(__file__)).split("/handlers")[0]

    full_file_path = current_directory + filename

    with open(full_file_path, "r", encoding="utf8") as file:
        data = json.load(file)
    return data


def is_valid_table_name(table_name):
    # Define a regular expression pattern to match valid table names
    valid_table_name_pattern = re.compile(r'^[a-zA-Z0-9_]+$')

    # Maximum table name length (adjust as needed)
    max_table_name_length = 50

    # Check if the table name matches the valid pattern and is not too long
    if len(table_name) <= max_table_name_length and valid_table_name_pattern.match(table_name):
        return True
    else:
        return False


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
    if "SELECT" in query or "OUTPUT" in query:

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
    

# Rest of your code...

def check_database_table_exists(table_name):
    try:
        if not is_valid_table_name(table_name):
            return False

        # Secure Query
        query = "IF EXISTS (SELECT * FROM information_schema.tables WHERE table_name = ?) SELECT 1 ELSE SELECT 0"
        result = db_query(query, (table_name,))

        if not result[0][0]:
            if table_name == "users":
                # Construct the SQL query
                query = """
                CREATE TABLE users (
                    id INT PRIMARY KEY NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    reset_token VARCHAR(255),
                    reset_token_timestamp DATETIMEOFFSET,
                    email VARCHAR(255) NOT NULL,
                    secret_key VARCHAR(255) NOT NULL,
                    role BIT NOT NULL
                )
                """
                db_query(query)

            elif table_name == "products":
                query = """
                CREATE TABLE products (
                    id INT PRIMARY KEY IDENTITY(1,1),
                    name NVARCHAR(255),
                    description NVARCHAR(255),
                    price NVARCHAR(255),
                    category NVARCHAR(255),
                    stock INT
                )
                """
                db_query(query)

            elif table_name == "reviews":
                query = """
                CREATE TABLE reviews (
                    id INT PRIMARY KEY IDENTITY(1,1),
                    product_id INT,
                    user_id INT,
                    rating INT,
                    review NVARCHAR(255)
                )
                """
                db_query(query)

            elif table_name == "emergency_codes":
                query = """
                CREATE TABLE emergency_codes (
                    id INT PRIMARY KEY IDENTITY(1,1),
                    code NVARCHAR(MAX),
                    born TIMESTAMP
                )
                """
                db_query(query)

            elif "_cart" in table_name:
                # Construct the SQL query
                query = f"""
                CREATE TABLE {table_name} (
                    product_id INT PRIMARY KEY IDENTITY(1,1),
                    quantity INT
                )
                """
                db_query(query)

            elif "all_orders" in table_name:
                query = """
                CREATE TABLE all_orders (
                    id INT PRIMARY KEY IDENTITY(1,1),
                    user_id INT,
                    order_date NVARCHAR(255)
                )
                """
                db_query(query)

            else:
                # Construct the SQL query
                query = f"""
                CREATE TABLE {table_name} (
                    id INT PRIMARY KEY IDENTITY(1,1),
                    products NVARCHAR(MAX),
                    total_price NVARCHAR(255),
                    shipping_address NVARCHAR(255),
                    order_date NVARCHAR(255)
                )
                """
                db_query(query)

    except Exception as e:
        print(e)