
# Horus Entry Exam - Fullstack Programmer Internship

[![Repository](https://img.shields.io/badge/GitHub-horus--naufal--exam-blue?logo=github)](https://github.com/Naufallabibb/horus-naufal-exam)

Proyek ini merupakan submission untuk Horus Entry Exam posisi Fullstack Programmer Internship. Aplikasi ini adalah sistem manajemen user dengan fitur CRUD (Create, Read, Update, Delete) yang terdiri dari REST API backend dan web frontend yang terintegrasi.

## 📋 Daftar Isi

* [Fitur Utama](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#-fitur-utama)
* [Teknologi yang Digunakan](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#-teknologi-yang-digunakan)
* [Struktur Folder](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#-struktur-folder)
* [Prasyarat](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#-prasyarat)
* [Instalasi](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#-instalasi)
  * [Backend Setup](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#1-backend-setup)
  * [Frontend Setup](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#2-frontend-setup)
  * [Database Setup](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#3-database-setup)
* [Menjalankan Aplikasi](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#-menjalankan-aplikasi)
* [API Endpoints](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#-api-endpoints)
* [Halaman Web](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#-halaman-web)
* [Database Schema](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#-database-schema)
* [Environment Variables](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#-environment-variables)
* [Testing](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#-testing)
* [Troubleshooting](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#-troubleshooting)
* [Kontributor](https://claude.ai/chat/095738c9-11d4-47f3-b8dc-388baa61e250#-kontributor)

## ✨ Fitur Utama

* **Autentikasi User** : Sistem login dan registrasi dengan password hashing
* **Manajemen User** : CRUD operations untuk data pengguna
* **Dashboard Interaktif** : Tampilan data user dalam bentuk tabel dengan fitur pencarian
* **Protected Routes** : Halaman dashboard yang hanya bisa diakses setelah login
* **Responsive Design** : Antarmuka yang dapat menyesuaikan berbagai ukuran layar
* **Validasi Data** : Validasi di sisi client dan server untuk integritas data

## 🛠 Teknologi yang Digunakan

### Backend

* **Python 3.8+** - Bahasa pemrograman utama
* **Flask** - Web framework untuk REST API
* **Flask-SQLAlchemy** - ORM untuk database operations
* **Flask-Migrate** - Database migration tool
* **Flask-JWT-Extended** - Authentication dengan JWT tokens
* **Flask-CORS** - Cross-Origin Resource Sharing support
* **Werkzeug** - Password hashing utilities
* **MySQL/PostgreSQL** - Database management system

### Frontend

* **Vue.js 3** - Progressive JavaScript framework
* **Vue Router** - Official router untuk Vue.js
* **Pinia/Vuex** - State management
* **Axios** - HTTP client untuk API calls
* **Bootstrap/Tailwind CSS** - CSS framework untuk styling

## 📁 Struktur Folder

```
horus-naufal-exam/
├── backend/                      # Backend REST API (Flask)
│   ├── app/                      # Main application package
│   │   ├── __init__.py          # Flask app initialization
│   │   ├── config.py            # Configuration settings
│   │   ├── extensions.py        # Flask extensions (db, migrate, jwt, cors)
│   │   ├── models/              # Database models
│   │   │   ├── __init__.py
│   │   │   └── user.py          # User model definition
│   │   ├── routes/              # API route handlers
│   │   │   ├── __init__.py
│   │   │   └── users.py         # User-related endpoints
│   │   ├── services/            # Business logic layer
│   │   │   ├── __init__.py
│   │   │   └── user_service.py  # User service operations
│   │   └── utils/               # Utility functions
│   │       ├── __init__.py
│   │       └── validators.py    # Input validation helpers
│   ├── migrations/              # Database migration files
│   ├── .env.example             # Environment variables template
│   ├── requirements.txt         # Python dependencies
│   └── run.py                   # Application entry point
│
├── frontend/                     # Frontend Web Interface (Vue.js)
│   ├── src/                     # Source code
│   │   ├── assets/              # Static assets (images, styles)
│   │   ├── components/          # Reusable Vue components
│   │   │   ├── UserTable.vue    # User list table component
│   │   │   └── SearchBar.vue    # Search functionality component
│   │   ├── views/               # Page components
│   │   │   ├── Login.vue        # Login page
│   │   │   ├── Register.vue     # Registration page
│   │   │   ├── Dashboard.vue    # Main dashboard (protected)
│   │   │   └── UpdateUser.vue   # User update form
│   │   ├── router/              # Vue Router configuration
│   │   │   └── index.js         # Route definitions
│   │   ├── store/               # State management
│   │   │   └── auth.js          # Authentication state
│   │   ├── services/            # API service layer
│   │   │   └── api.js           # Axios instance & API calls
│   │   ├── App.vue              # Root component
│   │   └── main.js              # Application entry point
│   ├── public/                  # Public static files
│   │   └── index.html           # HTML template
│   ├── .env.example             # Environment variables template
│   └── package.json             # Node dependencies
│
└── README.md                     # Documentation (this file)
```

### Penjelasan Struktur

#### **Backend (`/backend`)**

* **`app/config.py`** : Berisi konfigurasi aplikasi seperti database URI, secret key, JWT settings
* **`app/extensions.py`** : Inisialisasi extension Flask (SQLAlchemy, JWT, CORS, Migrate)
* **`app/models/user.py`** : Definisi model database User dengan kolom id, username, password, email, nama, created_at
* **`app/routes/users.py`** : Endpoint API untuk register, login, get users, update, dan delete
* **`app/services/user_service.py`** : Business logic untuk operasi user (hashing password, validasi, dll)
* **`app/utils/validators.py`** : Fungsi helper untuk validasi email, username, dll
* **`migrations/`** : Auto-generated oleh Flask-Migrate untuk version control database schema
* **`run.py`** : Entry point aplikasi yang menjalankan Flask development server

#### **Frontend (`/frontend`)**

* **`src/components/`** : Komponen Vue yang reusable (UserTable, SearchBar)
* **`src/views/`** : Halaman-halaman utama aplikasi (Login, Register, Dashboard, UpdateUser)
* **`src/router/index.js`** : Konfigurasi routing dan navigation guards untuk protected routes
* **`src/store/auth.js`** : State management untuk authentication (token, user data)
* **`src/services/api.js`** : Axios instance dengan base URL dan interceptors untuk handle API calls
* **`src/main.js`** : Entry point aplikasi Vue yang mount root component

## 📦 Prasyarat

Pastikan sistem Anda telah terinstall:

* **Python 3.8 atau lebih tinggi** - [Download Python](https://www.python.org/downloads/)
* **Node.js 14.x atau lebih tinggi** dan **npm** - [Download Node.js](https://nodejs.org/)
* **MySQL 5.7+** atau **PostgreSQL 12+** - Database server
* **Git** - Version control system

Verifikasi instalasi dengan command:

```bash
python --version
node --version
npm --version
mysql --version  # atau: psql --version
```

## 🚀 Instalasi

### 1. Backend Setup

#### a. Clone Repository

```bash
git clone https://github.com/Naufallabibb/horus-naufal-exam.git
cd horus-naufal-exam/backend
```

#### b. Buat Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### c. Install Dependencies

```bash
pip install -r requirements.txt
```

#### d. Setup Environment Variables

```bash
# Copy file .env.example menjadi .env
cp .env.example .env

# Edit file .env dengan text editor
# Sesuaikan konfigurasi database dan secret key
```

Contoh isi file `.env`:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database Configuration (MySQL example)
DATABASE_URL=mysql+pymysql://username:password@localhost/horus_naufal_db

# Atau untuk PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost/horus_naufal_db
```

#### e. Inisialisasi Database

```bash
# Jalankan migrasi database
flask db init      # (skip jika folder migrations sudah ada)
flask db migrate -m "Initial migration"
flask db upgrade
```

### 2. Frontend Setup

#### a. Masuk ke Folder Frontend

```bash
cd ../frontend
```

#### b. Install Dependencies

```bash
npm install
```

#### c. Setup Environment Variables

```bash
# Copy file .env.example menjadi .env
cp .env.example .env

# Edit file .env
```

Contoh isi file `.env`:

```env
VUE_APP_API_BASE_URL=http://localhost:5000
VUE_APP_PORT=3000
```

### 3. Database Setup

#### Untuk MySQL:

```bash
# Login ke MySQL
mysql -u root -p

# Buat database
CREATE DATABASE horus_naufal_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Buat user (opsional)
CREATE USER 'horus_user'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON horus_naufal_db.* TO 'horus_user'@'localhost';
FLUSH PRIVILEGES;

# Exit
EXIT;
```

#### Untuk PostgreSQL:

```bash
# Login ke PostgreSQL
psql -U postgres

# Buat database
CREATE DATABASE horus_naufal_db;

# Buat user (opsional)
CREATE USER horus_user WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE horus_naufal_db TO horus_user;

# Exit
\q
```

## ▶️ Menjalankan Aplikasi

### Jalankan Backend (Terminal 1)

```bash
cd backend
# Aktifkan virtual environment jika belum
source venv/bin/activate  # Linux/Mac
# atau: venv\Scripts\activate  # Windows

python run.py
```

Backend akan berjalan di: **http://localhost:5000**

### Jalankan Frontend (Terminal 2)

```bash
cd frontend
npm run serve
```

Frontend akan berjalan di: **http://localhost:3000**

Buka browser dan akses **http://localhost:3000** untuk menggunakan aplikasi.

## 🔌 API Endpoints

Base URL: `http://localhost:5000`

### Authentication

#### 1. Register User

```http
POST /users/register
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass123",
  "email": "john@example.com",
  "nama": "John Doe"
}
```

**Response (201 Created):**

```json
{
  "message": "Registrasi berhasil"
}
```

#### 2. Login User

```http
POST /users/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

**Response (200 OK):**

```json
{
  "message": "Login berhasil",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### User Management

#### 3. Get All Users

```http
GET /users
```

**Response (200 OK):**

```json
[
  {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "nama": "John Doe",
    "created_at": "2025-01-15T10:30:00"
  }
]
```

#### 4. Update User

```http
PUT /users/{id}
Content-Type: application/json

{
  "username": "johndoe_updated",
  "email": "john.new@example.com",
  "nama": "John Doe Updated"
}
```

**Response (200 OK):**

```json
{
  "message": "Data user berhasil diperbarui"
}
```

#### 5. Delete User

```http
DELETE /users/{id}
```

**Response (200 OK):**

```json
{
  "message": "User berhasil dihapus"
}
```

### Error Responses

**400 Bad Request:**

```json
{
  "error": "Username sudah digunakan"
}
```

**401 Unauthorized:**

```json
{
  "error": "Username atau password salah"
}
```

**404 Not Found:**

```json
{
  "error": "User tidak ditemukan"
}
```

## 🖥 Halaman Web

### 1. Login Page (`/login`)

* Input username dan password
* Validasi kredensial
* Redirect ke Dashboard setelah login sukses
* Link ke halaman Register

### 2. Register Page (`/register`)

* Form registrasi dengan field: username, password, email, nama
* Validasi input di client-side (format email, required fields)
* Notifikasi sukses/error
* Redirect ke Login setelah registrasi berhasil

### 3. Dashboard (`/dashboard`) - Protected Route

* Tampilan tabel semua user
* Fitur search/filter berdasarkan nama atau username
* Tombol Update untuk edit data user
* Tombol Delete dengan konfirmasi
* Tombol Logout
* **Proteksi** : Hanya bisa diakses setelah login

### 4. Update User Page (`/users/update/:id`)

* Form pre-filled dengan data user yang dipilih
* Update informasi user
* Tombol Kembali ke Dashboard
* Notifikasi sukses/error setelah update

## 🗄 Database Schema

### Tabel: `users`

| Kolom          | Tipe Data    | Constraint                  | Keterangan                               |
| -------------- | ------------ | --------------------------- | ---------------------------------------- |
| `id`         | INT/BIGINT   | PRIMARY KEY, AUTO_INCREMENT | Unique identifier                        |
| `username`   | VARCHAR(50)  | NOT NULL, UNIQUE            | Username untuk login                     |
| `password`   | VARCHAR(255) | NOT NULL                    | Password (hashed dengan bcrypt/werkzeug) |
| `email`      | VARCHAR(100) | NOT NULL, UNIQUE            | Email user                               |
| `nama`       | VARCHAR(100) | NOT NULL                    | Nama lengkap user                        |
| `created_at` | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP   | Waktu pembuatan akun                     |

#### SQL Schema:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    nama VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔐 Environment Variables

### Backend `.env`

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-very-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this

# Database Configuration
DATABASE_URL=mysql+pymysql://username:password@localhost/horus_naufal_db

# JWT Configuration (Optional)
JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hour in seconds

# CORS Configuration (Optional)
CORS_ORIGINS=http://localhost:3000
```

### Frontend `.env`

```env
# API Configuration
VUE_APP_API_BASE_URL=http://localhost:5000

# App Configuration (Optional)
VUE_APP_NAME=Horus User Management
```

## 🧪 Testing

### Backend Testing

```bash
cd backend
source venv/bin/activate

# Test dengan curl atau Postman
# Contoh: Test register endpoint
curl -X POST http://localhost:5000/users/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"Test123","email":"test@example.com","nama":"Test User"}'
```

### Frontend Testing

```bash
cd frontend

# Run unit tests (jika ada)
npm run test:unit

# Run e2e tests (jika ada)
npm run test:e2e
```

## 🔧 Troubleshooting

### Backend Issues

 **Problem** : `ModuleNotFoundError: No module named 'flask'`

```bash
# Pastikan virtual environment aktif dan install ulang dependencies
pip install -r requirements.txt
```

 **Problem** : Database connection error

```bash
# Periksa:
# 1. Database service berjalan (MySQL/PostgreSQL)
# 2. DATABASE_URL di .env sudah benar
# 3. Database sudah dibuat
# 4. User memiliki permission yang cukup
```

 **Problem** : Migration error

```bash
# Reset migrations
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Frontend Issues

 **Problem** : `npm ERR! code ELIFECYCLE`

```bash
# Clear npm cache dan install ulang
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

 **Problem** : CORS error di browser

```bash
# Pastikan Flask-CORS dikonfigurasi dengan benar di backend
# Check app/__init__.py dan pastikan CORS diinisialisasi
```

 **Problem** : API calls gagal

```bash
# Periksa:
# 1. Backend sudah berjalan di port 5000
# 2. VUE_APP_API_BASE_URL di .env frontend sudah benar
# 3. Tidak ada typo di endpoint URL
```

### Common Issues

**Port already in use:**

```bash
# Backend (port 5000)
# Windows: netstat -ano | findstr :5000
# Linux/Mac: lsof -ti:5000 | xargs kill -9

# Frontend (port 8080)
# Ubah port di vue.config.js atau jalankan:
npm run serve -- --port 3000
```

## 📝 Development Notes

### Best Practices yang Diterapkan:

* ✅ Separation of Concerns (models, routes, services)
* ✅ Password hashing untuk keamanan
* ✅ Input validation di client dan server
* ✅ Error handling yang comprehensive
* ✅ RESTful API design
* ✅ Clean code dan modular structure
* ✅ Environment-based configuration

### Improvements & Future Enhancements:

* [ ] Unit testing untuk backend dan frontend
* [ ] Pagination untuk list users
* [ ] Email verification saat registrasi
* [ ] Forgot password functionality
* [ ] Role-based access control (admin/user)
* [ ] Audit log untuk tracking changes
* [ ] Rate limiting untuk API endpoints
* [ ] Docker containerization

## 👨‍💻 Kontributor

**Naufal**

* GitHub: [@Naufallabibb](https://github.com/Naufallabibb)
* Repository: [horus-naufal-exam](https://github.com/Naufallabibb/horus-naufal-exam)

## 📄 Lisensi

Proyek ini dibuat untuk keperluan Horus Entry Exam - Fullstack Programmer Internship.

---

**Made with ❤️ for Horus Entry Exam**

Jika ada pertanyaan atau masalah, silakan buat issue di repository ini atau hubungi saya melalui GitHub.
