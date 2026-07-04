# Redis Caching Exercise Report

## Skenario
Implementasi caching sederhana menggunakan Redis untuk menyimpan hasil API call `get_weather()`.

---

## 1. Kode yang Dimodifikasi

### weather_api.py
```python
import requests
import time
import redis
import json
import os

# Koneksi Redis
r = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0,
    decode_responses=True  # agar otomatis decode dari bytes ke string
)

def get_weather(city):
    """
    Dapatkan data cuaca dengan caching Redis.
    Cache expiry: 5 menit (300 detik)
    """
    # Buat key cache yang unik untuk setiap kota
    cache_key = f"weather:{city}"
    
    # Cek apakah data ada di cache
    cached_data = r.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    # Jika tidak ada di cache, panggil API (simulasi lambat)
    time.sleep(2)  # Simulate slow API call (2 detik)
    
    # Simulasi response API
    weather_data = {
        "city": city,
        "temperature": 28 + (len(city) % 10),
        "condition": "Cerah" if len(city) % 2 == 0 else "Berawan",
        "humidity": 60 + (len(city) % 40),
        "timestamp": time.time()
    }
    
    # Simpan ke cache dengan expiry 5 menit (300 detik)
    r.setex(cache_key, 300, json.dumps(weather_data))
    
    return weather_data
```

---

## 2. Redis Commands yang Digunakan

| Command | Penjelasan |
|---|---|
| `SET key value` | Menyimpan data ke Redis |
| `GET key` | Mengambil data dari Redis |
| `SETEX key seconds value` | Menyimpan data ke Redis beserta waktu kadaluarsa (expiry) |
| `KEYS weather:*` | Melihat semua key cache untuk weather (untuk debugging) |

---

## 3. Hasil Testing

### First call (tidak ada cache)
```
First call to get_weather('Jakarta')...
First call time: 2.01s
```

### Second call (cache sudah ada)
```
Second call to get_weather('Jakarta') (cached)...
Second call time: 0.00s
```

### Perbandingan
- First call: ~2 detik (karena `time.sleep(2)`)
- Second call: ~0 detik (langsung dari Redis)
- **Percepatan: ~200x lebih cepat!**

---

## 4. Jawaban Pertanyaan

### a. Kenapa response time berbeda?
- **First call**: Tidak ada data di cache, jadi harus menunggu `time.sleep(2)` (simulasi API lambat).
- **Second call**: Data sudah ada di Redis, jadi langsung diambil tanpa perlu memanggil API lagi.

### b. Apa keuntungan caching?
1. **Percepatan waktu respon**: Mengurangi latensi karena data diambil dari memory (Redis) bukan dari disk/API eksternal.
2. **Mengurangi beban API**: Tidak perlu memanggil API berulang-ulang untuk data yang sama.
3. **Menghemat biaya**: Jika API berbayar, caching mengurangi jumlah request ke API.
4. **Meningkatkan scalability**: Aplikasi bisa menangani lebih banyak request tanpa harus menunggu API lambat.

### c. Kapan sebaiknya tidak menggunakan cache?
1. **Data yang selalu berubah**: Misalnya data real-time seperti harga saham detik demi detik (cache akan membuat data stale).
2. **Data sangat sensitif**: Misalnya data transaksi bank, lebih baik selalu ambil data terbaru dari database utama.
3. **Data yang jarang diakses**: Jika data hanya diakses sekali atau dua kali, caching tidak memberikan manfaat dan malah membuang memory.
4. **Operasi write-dominant**: Jika kebanyakan operasi adalah update/delete, caching akan sering di-invalidate dan tidak efisien.

---

## 5. Cara Menjalankan

### Persyaratan
- Docker dan Docker Compose sudah terinstall
- Redis sudah berjalan (bisa pakai `docker compose up -d redis` dari project Simple LMS)

### Langkah
1. Masuk ke folder project: `cd c:\simple-lms`
2. Nyalakan Redis: `docker compose up -d redis`
3. Install dependencies (jika belum): `pip install redis requests`
4. Jalankan testing: `python test_cache.py`

