-- Make a valid emergency code invalid --
-- TOTPHandler:remove_valid_emergency_code --
UPDATE emergency_codes
SET emergency_code_valid = 0
WHERE emergency_code = ? AND user_id = ?;


-- Update the TOTP attributes for a user --
-- TOTPHandler:update_totp --
UPDATE users SET secret_key = ?, secret_key_timestamp = ? WHERE id = ?;


-- Clear the Password Reset Token for a user --
-- UserManagement:set_reset_token_for_user --
UPDATE users SET password_reset_token = ? WHERE username = ?;
UPDATE users SET password_reset_token_timestamp = ? WHERE username = ?;
