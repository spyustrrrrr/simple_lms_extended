# 🎓 Simple LMS Extended API

Simple LMS Extended API adalah implementasi **RESTful API Backend** untuk aplikasi **Learning Management System (LMS)** sederhana. Proyek ini dibangun menggunakan **Django**, **Django Ninja**, dan **PostgreSQL**, serta dikemas menggunakan **Docker** agar proses instalasi, pengembangan, dan deployment menjadi lebih mudah.

API ini menerapkan sistem keamanan menggunakan **JWT (JSON Web Token)** dengan **RSA Asymmetric Encryption** serta **Role-Based Access Control (RBAC)** untuk memisahkan hak akses antara **Admin**, **Instructor**, dan **Student**.

---

## 🛠️ Tech Stack

| Teknologi | Keterangan |
|-----------|------------|
| **Language** | Python 3.11+ |
| **Framework** | Django, Django Ninja |
| **Database** | PostgreSQL |
| **Authentication** | JWT (`django-ninja-simple-jwt`) + RSA Key Pair |
| **Containerization** | Docker & Docker Compose |

---

## ⚙️ Prasyarat

Pastikan perangkat Anda telah menginstal:

- Docker
- Docker Compose

---

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone <repository-url>
cd <nama-folder-project>
```

---

### 2. Build dan Jalankan Container

Jalankan perintah berikut pada root project.

```bash
docker-compose up -d --build
```

Tunggu hingga proses build image, instalasi dependency, dan inisialisasi database selesai.

---

### 3. Generate RSA Key Pair

Sistem JWT menggunakan RSA Asymmetric Encryption sehingga perlu membuat pasangan **Private Key** dan **Public Key**.

Jalankan:

```bash
docker-compose exec web python manage.py make_rsa
```

> **Catatan**
>
> RSA Key hanya perlu dibuat **satu kali**.
>
> Jangan pernah membagikan **Private Key** kepada siapa pun.

---

### 4. Migrasi Database

Jalankan migrasi database PostgreSQL.

```bash
docker-compose exec web python manage.py migrate
```

---

### 5. Membuat Superuser

Buat akun administrator Django.

```bash
docker-compose exec web python manage.py createsuperuser
```

Ikuti instruksi yang muncul untuk mengisi:

- Username
- Email
- Password

> Setelah login ke Django Admin, ubah **Role** akun tersebut menjadi **Admin** agar sistem RBAC dapat berjalan dengan benar.

---

### 6. Seed Data (Opsional)

Jika project menyediakan script seed data, jalankan sesuai command yang tersedia untuk membuat data contoh seperti:

- Student
- Instructor
- Course
- Category
- Lesson

---

# 📖 Dokumentasi API

Setelah seluruh container berjalan, aplikasi dapat diakses pada:

| Layanan | URL |
|----------|-----|
| Django Admin | http://localhost:8002/admin/ |
| Swagger API Docs | http://localhost:8002/api/docs |

---

# 👨‍💼 Administrator Panel

Digunakan oleh:

- Admin
- Instructor

Fitur:

- CRUD User
- CRUD Course
- CRUD Lesson
- CRUD Category

Login menggunakan akun **Superuser** yang telah dibuat.

URL:

```
http://localhost:8002/admin/
```

---

# 📚 Swagger Documentation

Seluruh endpoint REST API dapat diuji melalui Swagger.

URL:

```
http://localhost:8002/api/docs
```

---

# 🔐 Testing JWT Authentication

### 1. Login

Gunakan endpoint berikut:

```
POST /api/auth/sign-in
```

Masukkan:

```json
{
  "username": "student",
  "password": "password"
}
```

---

### 2. Copy Access Token

Response akan menghasilkan token seperti:

```json
{
  "access": "eyJhbGc..."
}
```

Salin nilai **access** tersebut.

---

### 3. Authorize Swagger

Klik tombol **Authorize** di bagian atas Swagger.

Masukkan:

```
Bearer eyJhbGc...
```

Lalu klik:

- Authorize
- Close

---

### 4. Akses Endpoint yang Diproteksi

Setelah berhasil login, endpoint dengan ikon 🔒 dapat digunakan, misalnya:

```
GET /api/courses/dashboard/student
```

```
POST /api/courses/{course_id}/reviews
```

```
POST /api/courses/{course_id}/wishlist
```

```
GET /api/courses/{course_id}/progress
```

---

# 🔒 Role-Based Access Control (RBAC)

Project ini menerapkan tiga role utama.

| Role | Hak Akses |
|------|-----------|
| Admin | Mengelola seluruh data sistem |
| Instructor | Mengelola course dan lesson |
| Student | Mengakses dashboard, progress, wishlist, review, dan materi pembelajaran |

Apabila token JWT milik **Admin** atau **Instructor** digunakan untuk mengakses endpoint khusus Student, sistem akan mengembalikan response:

```
403 Forbidden
```

Begitu juga sebaliknya apabila Student mencoba mengakses endpoint Admin.

---

# 🧪 Contoh Alur Testing

1. Login sebagai Student.
2. Salin access token.
3. Klik **Authorize** di Swagger.
4. Tempelkan:

```
Bearer <access_token>
```

5. Akses endpoint Student.

Contoh:

```
GET /api/courses/dashboard/student
```

---

# 🛑 Menghentikan Server

Menghentikan container tanpa menghapus data database.

```bash
docker-compose stop
```

Menghapus seluruh container.

```bash
docker-compose down
```

Menghapus container beserta volume database.

```bash
docker-compose down -v
```

---

## 📁 Struktur Project

```text
simple_lms_experience/
│
├── .env.example               # Template environment variables
├── .gitignore                 # File yang diabaikan Git
├── docker-compose.yml         # Konfigurasi Docker Compose
├── Dockerfile                 # Docker image backend
├── manage.py                  # Entry point Django
├── requirements.txt           # Dependency Python
├── jwt-signing.pem            # RSA Private Key (Jangan di-push ke GitHub)
├── jwt-signing.pub            # RSA Public Key
│
├── core/                      # Konfigurasi utama Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── authentication/            # Modul autentikasi JWT & RSA
│   ├── __init__.py
│   ├── api.py                 # Endpoint login/logout/refresh token
│   ├── authentication.py      # Custom JWT Authentication
│   ├── permissions.py         # Role-Based Access Control (RBAC)
│   ├── schemas.py             # Schema request & response autentikasi
│   └── utils.py               # Helper autentikasi
│
├── users/                     # Manajemen user
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py              # Model User beserta Role
│   ├── schemas.py
│   ├── api.py
│   └── tests.py
│
├── courses/                   # Modul Learning Management System
│   ├── management/
│   │   └── commands/
│   │       └── seed.py        # Seed data awal
│   │
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_review.py
│   │   ├── 0003_section.py
│   │   └── 0004_lesson.py
│   │
│   ├── __init__.py
│   ├── admin.py               # Konfigurasi Django Admin
│   ├── api.py                 # Endpoint REST API
│   ├── apps.py
│   ├── models.py              # Model Course, Lesson, Review, Wishlist, Progress
│   ├── schemas.py             # Validasi Request & Response
│   ├── tests.py               # Unit Testing
│   └── views.py
│
├── media/                     # File upload (gambar course, dsb.)
│
├── static/                    # Static files
│
└── README.md                  # Dokumentasi proyek
```

# 👨‍💻 Developer

Simple LMS Extended API dibuat sebagai backend Learning Management System menggunakan:

- Django
- Django Ninja
- PostgreSQL
- Docker
- JWT Authentication (RSA)
- Role-Based Access Control (RBAC)