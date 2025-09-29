-- Correct SQLite database for Django User model

-- Create users table matching Django's AbstractUser + custom fields
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME,
    is_superuser BOOLEAN NOT NULL DEFAULT 0,
    username VARCHAR(150),  -- Can be blank/null
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL UNIQUE,
    is_staff BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    date_joined DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    native_language VARCHAR(2) NOT NULL DEFAULT 'en',
    is_premium BOOLEAN NOT NULL DEFAULT 0,
    subscription_end_date DATETIME,
    stripe_customer_id VARCHAR(255) NOT NULL DEFAULT '',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create user_progress table
CREATE TABLE IF NOT EXISTS user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content_type VARCHAR(50) NOT NULL,
    content_id INTEGER NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT 0,
    score REAL,
    completed_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    UNIQUE(user_id, content_type, content_id)
);

-- Insert test users with proper Django password hashes
INSERT INTO users (email, password, is_superuser, is_staff, native_language, is_premium, username, first_name, last_name) VALUES
('admin@test.com', 'pbkdf2_sha256$600000$abc123salt$QX9bqVB5vGhRGF5J1dQqzBJQHnNRqJ5oy4HqXTl1YjE=', 1, 1, 'id', 0, 'admin', 'Admin', 'User'),
('test@test.com', 'pbkdf2_sha256$600000$test123salt$mD5Py7RFJx8HGzG5Q4v9yBj4rOEQvYx8wWz3Bb2VcDQ=', 0, 0, 'id', 0, 'testuser', 'Test', 'User'),
('premium@test.com', 'pbkdf2_sha256$600000$prem123salt$rX8bPfA3vBhGGF5J4dQqzAJBHmNRqJ5py4HqXVl1ZjE=', 0, 0, 'id', 1, 'premiumuser', 'Premium', 'User');

-- Django system tables
CREATE TABLE IF NOT EXISTS django_migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS django_content_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE(app_label, model)
);

CREATE TABLE IF NOT EXISTS auth_permission (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL,
    codename VARCHAR(100) NOT NULL,
    FOREIGN KEY (content_type_id) REFERENCES django_content_type (id),
    UNIQUE(content_type_id, codename)
);

CREATE TABLE IF NOT EXISTS users_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    UNIQUE(user_id, group_id)
);

CREATE TABLE IF NOT EXISTS users_user_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (permission_id) REFERENCES auth_permission (id),
    UNIQUE(user_id, permission_id)
);

-- Learning app tables
CREATE TABLE IF NOT EXISTS learning_subjectgroup (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_key VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    order_number INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS learning_subject (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_key VARCHAR(100) NOT NULL UNIQUE,
    group_id INTEGER,
    name VARCHAR(200) NOT NULL,
    indonesian_name VARCHAR(200),
    description TEXT,
    order_number INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES learning_subjectgroup (id)
);

CREATE TABLE IF NOT EXISTS learning_examyear (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS learning_examsession (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year_id INTEGER NOT NULL,
    session_number INTEGER NOT NULL,
    name VARCHAR(200),
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (year_id) REFERENCES learning_examyear (id),
    UNIQUE(year_id, session_number)
);

-- Insert sample learning data
INSERT OR IGNORE INTO learning_subjectgroup (group_key, name, description, order_number) VALUES
('A', 'Aグループ', '人間と社会領域', 1),
('B', 'Bグループ', 'こころとからだのしくみ領域', 2),
('C', 'Cグループ', '介護過程・総合問題', 3);

INSERT OR IGNORE INTO learning_examyear (year, description) VALUES
(2025, '2025年度介護福祉士国家試験'),
(2024, '2024年度介護福祉士国家試験'),
(2023, '2023年度介護福祉士国家試験');

INSERT OR IGNORE INTO learning_examsession (year_id, session_number, name) VALUES
(1, 37, '2025年度第37回介護福祉士国家試験'),
(2, 36, '2024年度第36回介護福祉士国家試験'),
(3, 35, '2023年度第35回介護福祉士国家試験');

-- Insert subjects
INSERT OR IGNORE INTO learning_subject (subject_key, group_id, name, indonesian_name, order_number) VALUES
('human_dignity_independence', 1, '人間の尊厳と自立', 'Martabat dan Kemandirian Manusia', 1),
('care_basics', 1, '介護の基本', 'Dasar-dasar Perawatan', 2),
('social_understanding', 1, '社会の理解', 'Pemahaman Sosial', 3),
('human_relations_communication', 1, '人間関係とコミュニケーション', 'Hubungan Manusia dan Komunikasi', 4),
('communication_technology', 1, 'コミュニケーション技術', 'Teknologi Komunikasi', 5),
('life_support_technology', 1, '生活支援技術', 'Teknologi Dukungan Kehidupan', 6),
('mind_body_mechanism', 2, 'こころとからだのしくみ', 'Mekanisme Pikiran dan Tubuh', 7),
('development_aging', 2, '発達と老化の理解', 'Pemahaman Perkembangan dan Penuaan', 8),
('dementia_understanding', 2, '認知症の理解', 'Pemahaman Demensia', 9),
('disability_understanding', 2, '障害の理解', 'Pemahaman Disabilitas', 10),
('medical_care', 2, '医療的ケア', 'Perawatan Medis', 11),
('care_process', 3, '介護過程', 'Proses Perawatan', 12),
('comprehensive_problems', 3, '総合問題', 'Masalah Komprehensif', 13);

-- Insert essential Django migration records
INSERT OR IGNORE INTO django_migrations (app, name) VALUES
('contenttypes', '0001_initial'),
('auth', '0001_initial'),
('users', '0001_initial'),
('learning', '0001_initial'),
('sessions', '0001_initial');

-- Insert content types
INSERT OR IGNORE INTO django_content_type (app_label, model) VALUES
('users', 'user'),
('users', 'userprogress'),
('learning', 'subjectgroup'),
('learning', 'subject'),
('learning', 'examyear'),
('learning', 'examsession');

-- Display created users for verification
SELECT 'Created users:' AS info;
SELECT email, is_superuser, is_staff, is_premium FROM users;