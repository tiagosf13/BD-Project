USE [p2g3]

-- Check if the table exists -- Create the table if it does not exist
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'emergency_codes')
BEGIN
    -- Table: public.emergency_codes -- Table for storing emergency codes data
    CREATE TABLE emergency_codes (
        user_id INT NOT NULL,
        emergency_code INT NOT NULL,
        emergency_code_valid BIT NOT NULL,
        emergency_code_timestamp DATETIMEOFFSET NOT NULL,

        CONSTRAINT EMERGENCY_CODES_PK 
            PRIMARY KEY (user_id, emergency_code),

        CONSTRAINT EMERGENCY_CODES_FK_user_id
            FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
END

-- Path: src/queries/create_emergency_codes_table.sql