# Simple LMS (Learning Management System)

Project ini adalah backend sistem LMS yang dibangun menggunakan **Django**, **Django Ninja**, **PostgreSQL**, dan **Docker**. Project ini mencakup pemodelan data tingkat lanjut, optimasi query, dan sistem autentikasi JWT dengan Role-Based Access Control (RBAC).

---

## 🎯 Fitur & Capaian Project

### 1. Data Modeling & Optimization (Progress 2)
* **Skema Database**: Implementasi relasi yang tepat antara User, Category (self-referencing), Course, Lesson, Enrollment, dan Progress.
* **Optimasi Query**: Penggunaan `select_related` dan `prefetch_related` untuk mengatasi masalah N+1.
* **Custom Managers**: Implementasi `Course.objects.for_listing()` dan `Enrollment.objects.for_student_dashboard()`.
* **Django Admin**: Konfigurasi antarmuka admin yang informatif dengan fitur search, filter, dan inline models.

### 2. REST API & Authentication (Progress 3)
* **Django Ninja**: Framework API berbasis Type Hints yang cepat dan efisien.
* **JWT Authentication**: Secure login menggunakan `django-ninja-jwt`.
* **RBAC (Role-Based Access Control)**: Permission sistem menggunakan decorator `@is_instructor`, `@is_admin`, dan `@is_student`.
* **Swagger Documentation**: Dokumentasi API interaktif yang tersedia secara otomatis.

---

## 🛠️ Teknologi

* **Backend**: Python 3.11, Django 5.2+
* **API Framework**: Django Ninja, Pydantic
* **Database**: PostgreSQL (Production-ready) & SQLite (Local testing)
* **Authentication**: JWT (JSON Web Token)
* **Containerization**: Docker & Docker Compose

---

## 📸 Screenshots

### 1. API Documentation (Swagger UI)
![Swagger UI](images/Screenshot 2026-04-24 171431.png)

### 2. Django Admin - Course Management
![Admin Courses](images/Screenshot 2026-04-24 171442.png)

### 3. JWT Authentication & Endpoints
![API Testing](images/Screenshot 2026-04-24 171453.png)

*(Screenshots lama dapat dilihat di folder `images/`)*

---

## 📁 Struktur Project

```text
simple-lms/
│
├── config/              # Konfigurasi utama Django & API Entry Point
├── courses/             # App LMS (Course, Lesson, Enrollment, Progress)
│   ├── api.py           # Endpoint API Courses
│   ├── schemas.py       # Pydantic Schemas
│   └── permissions.py   # RBAC Decorators
├── users/               # App User (Custom User Model & Auth)
│   ├── api.py           # Endpoint API Auth
│   └── schemas.py       # Pydantic Schemas
├── images/              # Dokumentasi screenshot
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env                 # Konfigurasi environment
└── README.md
```

---

## 🚀 Cara Menjalankan Project

### 1. Persiapan
```bash
git clone https://github.com/Sigit02825/simple-lms.git
cd simple-lms
```

### 2. Jalankan dengan Docker
```bash
docker compose up --build
```

### 3. Setup Database & Data Awal
```bash
# Jalankan migrasi
docker compose exec web python manage.py migrate

# Isi data dummy (Users, Courses, Lessons)
docker compose exec web python seed_db.py
```

---

## 🔗 Endpoint Utama

* **API Documentation (Swagger)**: `http://localhost:8000/api/docs`
* **Admin Panel**: `http://localhost:8000/admin/`
* **Auth Endpoints**:
    * Login (Get Token): `POST /api/token/pair`
    * Register: `POST /api/auth/register`
    * My Profile: `GET /api/auth/me`

---

## 👤 Author

**Nama**: Sigit Ilham
**Project**: Tugas Besar Simple LMS - Server Side Programming
**Status**: Completed (Progress 1, 2, & 3)
