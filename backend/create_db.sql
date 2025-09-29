-- SQLite database initialization script for Japanese Learning Platform

-- Create users table (custom User model)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME,
    is_superuser BOOLEAN NOT NULL DEFAULT 0,
    email VARCHAR(254) NOT NULL UNIQUE,
    is_staff BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    date_joined DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    native_language VARCHAR(2) NOT NULL DEFAULT 'id',
    is_premium BOOLEAN NOT NULL DEFAULT 0,
    subscription_end_date DATETIME
);

-- Insert sample users with hashed passwords
-- Password: admin123 (pbkdf2_sha256 hash)
INSERT OR IGNORE INTO users (email, password, is_superuser, is_staff, native_language)
VALUES ('admin@test.com', 'pbkdf2_sha256$600000$admin123hash$dummyhash123', 1, 1, 'id');

-- Password: test123
INSERT OR IGNORE INTO users (email, password, is_superuser, is_staff, native_language)
VALUES ('test@test.com', 'pbkdf2_sha256$600000$test123hash$dummyhash123', 0, 0, 'id');

-- Password: premium123
INSERT OR IGNORE INTO users (email, password, is_superuser, is_staff, native_language, is_premium)
VALUES ('premium@test.com', 'pbkdf2_sha256$600000$premium123hash$dummyhash123', 0, 0, 'id', 1);

-- Create Django migrations table
CREATE TABLE IF NOT EXISTS django_migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create sessions table
CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date DATETIME NOT NULL
);

-- Create content types table
CREATE TABLE IF NOT EXISTS django_content_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL
);

-- Create auth permissions table
CREATE TABLE IF NOT EXISTS auth_permission (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL,
    codename VARCHAR(100) NOT NULL
);

-- Learning app tables
CREATE TABLE IF NOT EXISTS learning_subject (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_key VARCHAR(100) NOT NULL UNIQUE,
    group_key VARCHAR(10) NOT NULL,
    name VARCHAR(200) NOT NULL,
    indonesian_name VARCHAR(200),
    description TEXT,
    order_number INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
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
    FOREIGN KEY (year_id) REFERENCES learning_examyear (id)
);

-- Insert sample data
INSERT OR IGNORE INTO learning_examyear (year, description, is_active) VALUES
(2025, '2025年度介護福祉士国家試験', 1),
(2024, '2024年度介護福祉士国家試験', 1),
(2023, '2023年度介護福祉士国家試験', 1);

INSERT OR IGNORE INTO learning_examsession (year_id, session_number, name, is_active) VALUES
(1, 37, '2025年度第37回介護福祉士国家試験', 1),
(2, 36, '2024年度第36回介護福祉士国家試験', 1),
(3, 35, '2023年度第35回介護福祉士国家試験', 1);

-- Insert subjects based on CSV data
INSERT OR IGNORE INTO learning_subject (subject_key, group_key, name, indonesian_name, order_number) VALUES
('human_dignity_independence', 'A', '人間の尊厳と自立', 'Martabat dan Kemandirian Manusia', 1),
('care_basics', 'A', '介護の基本', 'Dasar-dasar Perawatan', 2),
('social_understanding', 'A', '社会の理解', 'Pemahaman Sosial', 3),
('human_relations_communication', 'A', '人間関係とコミュニケーション', 'Hubungan Manusia dan Komunikasi', 4),
('communication_technology', 'A', 'コミュニケーション技術', 'Teknologi Komunikasi', 5),
('life_support_technology', 'A', '生活支援技術', 'Teknologi Dukungan Kehidupan', 6),
('mind_body_mechanism', 'B', 'こころとからだのしくみ', 'Mekanisme Pikiran dan Tubuh', 7),
('development_aging', 'B', '発達と老化の理解', 'Pemahaman Perkembangan dan Penuaan', 8),
('dementia_understanding', 'B', '認知症の理解', 'Pemahaman Demensia', 9),
('disability_understanding', 'B', '障害の理解', 'Pemahaman Disabilitas', 10),
('medical_care', 'B', '医療的ケア', 'Perawatan Medis', 11),
('care_process', 'C', '介護過程', 'Proses Perawatan', 12),
('comprehensive_problems', 'C', '総合問題', 'Masalah Komprehensif', 13);