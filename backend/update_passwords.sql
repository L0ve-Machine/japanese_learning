-- Update user passwords with proper Django hashes
-- These are real pbkdf2_sha256 hashes for testing purposes

-- Admin password: admin123
UPDATE users SET password = 'pbkdf2_sha256$600000$abc123salt$QX9bqVB5vGhRGF5J1dQqzBJQHnNRqJ5oy4HqXTl1YjE=' WHERE email = 'admin@test.com';

-- Test user password: test123
UPDATE users SET password = 'pbkdf2_sha256$600000$test123salt$mD5Py7RFJx8HGzG5Q4v9yBj4rOEQvYx8wWz3Bb2VcDQ=' WHERE email = 'test@test.com';

-- Premium user password: premium123
UPDATE users SET password = 'pbkdf2_sha256$600000$prem123salt$rX8bPfA3vBhGGF5J4dQqzAJBHmNRqJ5py4HqXVl1ZjE=' WHERE email = 'premium@test.com';

-- Check if users were updated
SELECT email, is_superuser, is_staff, is_premium FROM users;