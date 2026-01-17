# Cara Mengatur Radius Kantor - Panduan Cepat

## 🚀 Langkah Cepat

### 1. Dapatkan Koordinat Kantor
- Buka **Google Maps**: https://www.google.com/maps
- Cari alamat kantor
- **Klik kanan** pada lokasi → Pilih "Koordinat"
- Catat koordinat (contoh: `-6.2088, 106.8456`)

### 2. Edit File config.py
Buka file `config.py` dan ubah bagian ini:

```python
# Geolocation Settings
OFFICE_LATITUDE = -6.2088      # Ganti dengan latitude kantor Anda
OFFICE_LONGITUDE = 106.8456    # Ganti dengan longitude kantor Anda
GEO_RADIUS_METERS = 100        # Ganti dengan radius (dalam meter)
```

### 3. Simpan dan Restart
- Simpan file `config.py`
- **Restart aplikasi** (hentikan dengan Ctrl+C, lalu jalankan lagi `python app.py`)

---

## 📍 Parameter yang Perlu Diatur

| Parameter | Deskripsi | Contoh | Default |
|-----------|-----------|--------|---------|
| `OFFICE_LATITUDE` | Koordinat lintang kantor | `-6.2088` | Jakarta |
| `OFFICE_LONGITUDE` | Koordinat bujur kantor | `106.8456` | Jakarta |
| `GEO_RADIUS_METERS` | Radius dalam meter | `100` | 100 meter |

---

## 💡 Rekomendasi Radius

- **50-100 meter**: Kantor kecil / gedung tunggal
- **100-200 meter**: Kantor menengah / kompleks kantor ⭐ **Direkomendasikan**
- **200-500 meter**: Area kantor luas / kawasan industri
- **> 500 meter**: Tidak disarankan (terlalu luas)

---

## 🔧 Alternatif: Menggunakan Environment Variables

### Buat/Edit file `.env`:
```env
OFFICE_LATITUDE=-6.2088
OFFICE_LONGITUDE=106.8456
GEO_RADIUS_METERS=150
```

File `config.py` sudah mendukung environment variables, jadi tidak perlu diubah lagi.

---

## ✅ Contoh Konfigurasi

### Jakarta Pusat (Radius 100m)
```python
OFFICE_LATITUDE = -6.2088
OFFICE_LONGITUDE = 106.8456
GEO_RADIUS_METERS = 100
```

### Bandung (Radius 200m - Area Luas)
```python
OFFICE_LATITUDE = -6.9175
OFFICE_LONGITUDE = 107.6191
GEO_RADIUS_METERS = 200
```

### Surabaya (Radius 75m - Gedung Kecil)
```python
OFFICE_LATITUDE = -7.2575
OFFICE_LONGITUDE = 112.7521
GEO_RADIUS_METERS = 75
```

---

## ⚠️ Catatan Penting

1. **Koordinat Format**: Gunakan titik (`.`) bukan koma (`,`)
   - ✅ Benar: `-6.2088`
   - ❌ Salah: `-6,2088`

2. **Restart Aplikasi**: Setelah mengubah config, **WAJIB restart** aplikasi

3. **Testing**: Setelah mengatur, test check-in dari berbagai lokasi:
   - ✅ Dari dalam kantor → Harus berhasil
   - ✅ Dari luar tapi dalam radius → Harus berhasil
   - ❌ Dari luar radius → Harus ditolak

---

## 🔍 Troubleshooting

**Presensi selalu ditolak meskipun di kantor?**
- Perbesar radius (misalnya dari 100m menjadi 150m)
- Verifikasi koordinat dengan Google Maps

**Presensi diterima meskipun di luar kantor?**
- Perkecil radius (misalnya dari 200m menjadi 100m)
- Perbaiki koordinat agar lebih tepat

**Perubahan tidak diterapkan?**
- Pastikan sudah **restart aplikasi**
- Cek tidak ada typo di file config

---

## 📖 Tutorial Lengkap

Untuk tutorial lebih detail, lihat: `TUTORIAL_ATUR_RADIUS_KANTOR.md`
