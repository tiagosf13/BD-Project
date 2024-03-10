import pyotp, qrcode, io, base64, json
from datetime import datetime
from handlers.DataBaseCoordinator import db_query
from handlers.UserManagement import generate_emergency_code


def generate_emergency_codes(id, n_codes=10, code_length=6, reset=False):

    if check_existence_emergency_codes(id) and not reset:
        return get_user_emergency_codes(id)

    # Generate n_codes emergency codes, each with code_length characters (Upper case letters, Lower case letters, Special characters and numbers)
    emergency_codes = {}

    for i in range(n_codes):
        
        # Generate a random code with code_length numbers
        emergency_codes[generate_emergency_code()] = True
    store_emergency_codes(id, emergency_codes)

    return emergency_codes

def get_user_emergency_codes(id):
    if check_existence_emergency_codes(id):
        query = "SELECT code FROM emergency_codes WHERE id = %s"
        result = db_query(query, (id,))
        if result:
            return result[0][0]
    return None

def remove_valid_emergency_code(id, code):
    if check_existence_emergency_codes(id):
        emergency_codes = get_user_emergency_codes(id)
        if code in emergency_codes:
            emergency_codes[code] = False
            store_emergency_codes(id, emergency_codes)
            return True
    return False

def check_existence_emergency_codes(id):
    query = "SELECT EXISTS(SELECT * FROM emergency_codes WHERE id = %s)"
    result = db_query(query, (id,))
    if result[0][0]:
        return True
    return False

def store_emergency_codes(id, emergency_codes):

    if check_existence_emergency_codes(id):
        # Delete the entry
        query = "DELETE FROM emergency_codes WHERE id = %s"
        db_query(query, (id,))

    # Convert dictionary to a JSON string
    codes_json = json.dumps(emergency_codes)

    query = "INSERT INTO emergency_codes (id, code, born) VALUES (%s, %s, %s);"
    db_query(query, (id, codes_json, datetime.now()))


# Function to generate a TOTP secret for a user
def generate_totp_secret():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=30)
    totp_secret_timestamp = datetime.now()
    return totp.secret, totp_secret_timestamp

def generate_totp_atributes(username, qr_code=True):
    # Fetch the secret key for the user
    secret_key, secret_key_timestamp = generate_totp_secret()
    
    if qr_code:
        qr_code_base64 = generate_qr_code(secret_key, username)
    else:
        qr_code_base64 = None
    
    return secret_key, secret_key_timestamp, qr_code_base64

def generate_qr_code(secret_key, username):
    # Generate QR code image
    totp = pyotp.TOTP(secret_key)
    qr = qrcode.make(totp.provisioning_uri(name=username, issuer_name='DETI Store'))

    # Convert QR code image to base64
    qr_code = io.BytesIO()
    qr.save(qr_code, format='PNG')
    qr_code_base64 = base64.b64encode(qr_code.getvalue()).decode('utf-8').strip()
    return qr_code_base64

def store_totp_stage(temp_id, username, secret_key, secret_key_timestamp, email, hashed_password):
    # Store the secret key securely for each user, maybe in a database
    # For demonstration purposes, a dictionary is used here to store secrets
    
    query = "INSERT INTO totp_temp (id, username, secret_key, secret_key_timestamp, email, password) VALUES (%s, %s, %s, %s, %s, %s);"
    db_query(query, (temp_id, username, secret_key, secret_key_timestamp, email, hashed_password))

def update_totp(id, secret_key, secret_key_timestamp):
    # Store the secret key securely for each user, maybe in a database
    # For demonstration purposes, a dictionary is used here to store secrets
    
    query = "UPDATE users SET secret_key = %s, secret_key_timestamp = %s WHERE id = %s;"
    db_query(query, (secret_key, secret_key_timestamp, id))


def verify_totp_code(id, token, table_name, username=None):
    query = f"SELECT secret_key, secret_key_timestamp FROM {table_name} WHERE id = %s"

    # Fetch the secret key for the user and the secret_key_timestamp
    result = db_query(query, (id,))
    if result:
        secret_key = result[0][0] 

        totp = pyotp.TOTP(secret_key)
        is_verified = totp.verify(token)
        if is_verified:
            return True
        else:
            return False
    return False




def get_totp_secret(id):
    # Fetch the secret key for the user
    query = "SELECT secret_key FROM users WHERE id = %s"
    result = db_query(query, (id,))

    if result:
        secret_key = result[0][0]
        return secret_key
    
    return None

def get_totp_atributes(id):

    # Fetch the secret key for the user
    query = "SELECT username, email, password, secret_key, secret_key_timestamp FROM totp_temp WHERE id = %s"
    result = db_query(query, (id,))

    if result:
        username = result[0][0]
        email = result[0][1]
        hashed_password = result[0][2]
        secret_key = result[0][3]
        secret_key_timestamp = result[0][4]
        return username, email, hashed_password, secret_key, secret_key_timestamp
    
    return None, None, None