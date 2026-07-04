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
    
    # Simulasi response API (karena api.example.com tidak ada)
    # Kalau ingin API nyata, bisa gunakan OpenWeatherMap, tapi untuk latihan cukup simulasi
    weather_data = {
        "city": city,
        "temperature": 28 + (len(city) % 10),  # Simulasi suhu acak
        "condition": "Cerah" if len(city) % 2 == 0 else "Berawan",
        "humidity": 60 + (len(city) % 40),
        "timestamp": time.time()
    }
    
    # Simpan ke cache dengan expiry 5 menit (300 detik)
    r.setex(cache_key, 300, json.dumps(weather_data))
    
    return weather_data

