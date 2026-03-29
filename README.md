# Simple LMS (Learning Management System)

Project ini adalah backend sederhana untuk sistem LMS menggunakan **Django**, **Django REST Framework**, dan **Docker**.

---

## Fitur Utama

* API Course (Kursus)
* API Lesson (Materi)
* API Enrollment (Pendaftaran)
* Authentication menggunakan JWT
* Dockerized (mudah dijalankan)

---

## Teknologi

* Python
* Django
* Django REST Framework
* JWT Authentication
* Docker & Docker Compose

---

## Screenshot

### 1. Docker & Container Berjalan

![Docker](Screenshot 2026-03-29 205957.png)

### 2. Server Django Berjalan

![Server](Screenshot 2026-03-29 205643.png)

### 3. Project Structure

![Structure](Screenshot 2026-03-29 210102.png)

### 4. Django Login

![JWT](Screenshot 2026-03-29 210131.png)

### 5. Install Django

![Install](Screenshot 2026-03-29 205652.png)

---

## Struktur Project

```id="tqcbpg"
simple-lms/
│
├── config/              # Konfigurasi utama Django
├── courses/             # App LMS (Course, Lesson, Enrollment)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── screenshots/         # Folder gambar
└── README.md
```

---

## Cara Menjalankan Project

### 1. Clone Repository

```bash id="e6p0u1"
git clone https://github.com/Sigit02825/simple-lms.git
cd simple-lms
```

---

### 2. Jalankan Docker

```bash id="c5f7zv"
docker compose up --build
```

---

### 3. Jalankan Migration

```bash id="dnx7ml"
docker compose exec web python manage.py migrate
```

---

### 4. Buat Superuser

```bash id="g1l0dn"
docker compose exec web python manage.py createsuperuser
```

---

### 5. Akses Aplikasi

* Admin Panel:
  http://localhost:8000/admin/

* API Root:
  http://localhost:8000/api/

---

## Authentication (JWT)

### Login

```http id="lgp3t5"
POST /api/token/
```

Body:

```json id="9xxy1k"
{
  "username": "admin",
  "password": "sigitilham"
}
```

Response:

```json id="9f4dr3"
{
  "access": "admin",
  "refresh": "sigitilham"
}
```

---

### Gunakan Token

Tambahkan header:

```id="a6gm3w"
Authorization: Bearer <access_token>
```

---

## Endpoint API

* `/api/courses/`
* `/api/lessons/`
* `/api/enrollments/`

---

## Testing API

Gunakan:

* Postman
* Thunder Client (VS Code)

---

## Author

Nama: Sigit Ilham
Project: Simple LMS - Docker & Django Foundation

---
