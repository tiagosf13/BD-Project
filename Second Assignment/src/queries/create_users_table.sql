USE [BD-Project]

-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'users')
BEGIN
    -- Table: public.users -- Table for storing user data
    CREATE TABLE users (
        user_id INT NOT NULL,
        username VARCHAR(255) NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        password_reset_token VARCHAR(255),
        password_reset_token_timestamp DATETIMEOFFSET,
        email VARCHAR(255) NOT NULL,
        totp_secret_key VARCHAR(255) NOT NULL,
        totp_secret_key_timestamp DATETIMEOFFSET NOT NULL,
        admin_role BIT NOT NULL,
        PRIMARY KEY (user_id),
    );

    -- Null User -> To be used when an account gets deleted
    INSERT INTO users
    VALUES (
        -1,                 -- ID
        '[DELETED USER]',   -- username
        'null',             -- hashed_password
         null,              -- password_reset_token
         null,              -- password_reset_token_timestamp
        'null',             -- email
        'null',             -- totp_secret_key
        '1970-01-01',       -- totp_secret_key_timestamp
        0                   -- admin_role
    )
END

-- Path: src/queries/create_carts_table.sql