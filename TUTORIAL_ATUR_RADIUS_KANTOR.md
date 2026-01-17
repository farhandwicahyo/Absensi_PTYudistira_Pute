# Tutorial: Cara Mengatur Radius Kantor

Panduan lengkap untuk mengatur koordinat dan radius kantor untuk sistem presensi geolocation.

---

## 📋 Daftar Isi

1. [Pengenalan](#pengenalan)
2. [Cara Mendapatkan Koordinat Kantor](#cara-mendapatkan-koordinat-kantor)
3. [Mengatur Radius di File Config](#mengatur-radius-di-file-config)
4. [Mengatur Radius dengan Environment Variables](#mengatur-radius-dengan-environment-variables)
5. [Tips dan Rekomendasi](#tips-dan-rekomendasi)
6. [Troubleshooting](#troubleshooting)
7. [Contoh Konfigurasi](#contoh-konfigurasi)

---

## 🎯 Pengenalan

Sistem presensi menggunakan **geolocation** untuk memastikan karyawan melakukan check-in/check-out di area kantor. Ada 3 parameter yang perlu dikonfigurasi:

1. **OFFICE_LATITUDE** - Koordinat latitude (lintang) kantor
2. **OFFICE_LONGITUDE** - Koordinat longitude (bujur) kantor
3. **GEO_RADIUS_METERS** - Radius dalam meter yang diizinkan untuk presensi

**Default saat ini:**
- Latitude: `-6.2088` (Jakarta)
- Longitude: `106.8456` (Jakarta)
- Radius: `100` meter

---

## 📍 Cara Mendapatkan Koordinat Kantor

### Metode 1: Menggunakan Google Maps (Paling Mudah)

1. **Buka Google Maps** di browser: https://www.google.com/maps

2. **Cari alamat kantor** Anda di search box

3. **Klik kanan** pada lokasi kantor yang tepat di peta

4. **Pilih "Koordinat"** atau "Copy coordinates"

5. Anda akan mendapatkan koordinat dalam format:
   ```
   -6.2088, 106.8456
   ```
   - Angka pertama adalah **Latitude** (lintang)
   - Angka kedua adalah **Longitude** (bujur)

6. **Catat koordinat** tersebut untuk digunakan di konfigurasi

### Metode 2: Menggunakan GPS di Smartphone

1. Buka aplikasi **Google Maps** di smartphone
2. Pastikan GPS aktif
3. Pergi ke lokasi kantor
4. Tekan dan tahan pada lokasi di peta
5. Koordinat akan muncul di bagian bawah
6. Catat koordinat tersebut

### Metode 3: Menggunakan Website Lain

- **LatLong.net**: https://www.latlong.net/
- **GPS Coordinates**: https://www.gps-coordinates.net/
- **OpenStreetMap**: https://www.openstreetmap.org/

---

## ⚙️ Mengatur Radius di File Config

### Langkah 1: Buka File config.py

Buka file `config.py` yang berada di root folder project dengan text editor atau IDE.

### Langkah 2: Cari Bagian Geolocation Settings

Cari bagian berikut di file `config.py`:

```python
# Geolocation Settings
OFFICE_LATITUDE = -6.2088  # Contoh koordinat Jakarta
OFFICE_LONGITUDE = 106.8456
GEO_RADIUS_METERS = 100  # Radius dalam meter
```

### Langkah 3: Ubah Nilai Konfigurasi

Ganti nilai sesuai dengan koordinat dan radius kantor Anda:

```python
# Geolocation Settings
OFFICE_LATITUDE = -6.2088      # Ganti dengan latitude kantor Anda
OFFICE_LONGITUDE = 106.8456    # Ganti dengan longitude kantor Anda
GEO_RADIUS_METERS = 100        # Ganti dengan radius yang diinginkan (dalam meter)
```

**Contoh:**
```python
# Geolocation Settings - Kantor di Bandung
OFFICE_LATITUDE = -6.9175      # Latitude Bandung
OFFICE_LONGITUDE = 107.6191    # Longitude Bandung
GEO_RADIUS_METERS = 150        # Radius 150 meter
```

### Langkah 4: Simpan File

Simpan perubahan di file `config.py`.

### Langkah 5: Restart Aplikasi

**PENTING:** Setelah mengubah konfigurasi, **restart aplikasi** agar perubahan diterapkan:

1. Hentikan aplikasi yang sedang berjalan (Ctrl + C di terminal)
2. Jalankan lagi aplikasi:
   ```bash
   python app.py
   ```

---

## 🔐 Mengatur Radius dengan Environment Variables

Alternatif lain adalah menggunakan **environment variables** untuk konfigurasi. Ini berguna jika Anda tidak ingin mengubah file `config.py` langsung.

### Langkah 1: Buat atau Edit File .env

Buat file `.env` di root folder project (jika belum ada), atau edit yang sudah ada.

### Langkah 2: Tambahkan Environment Variables

Tambahkan baris berikut di file `.env`:

```env
OFFICE_LATITUDE=-6.2088
OFFICE_LONGITUDE=106.8456
GEO_RADIUS_METERS=100
```

**Contoh untuk kantor di Surabaya:**
```env
OFFICE_LATITUDE=-7.2575
OFFICE_LONGITUDE=112.7521
GEO_RADIUS_METERS=200
```

### Langkah 3: Update config.py untuk Membaca Environment Variables

Edit file `config.py` untuk membaca dari environment variables:

```python
# Geolocation Settings
OFFICE_LATITUDE = float(os.environ.get('OFFICE_LATITUDE', -6.2088))
OFFICE_LONGITUDE = float(os.environ.get('OFFICE_LONGITUDE', 106.8456))
GEO_RADIUS_METERS = int(os.environ.get('GEO_RADIUS_METERS', 100))
```

**Catatan:** Jika file `config.py` belum mendukung environment variables untuk geolocation, Anda perlu menambahkannya.

### Langkah 4: Restart Aplikasi

Restart aplikasi agar perubahan diterapkan.

---

## 💡 Tips dan Rekomendasi

### 1. **Pemilihan Radius**

- **50-100 meter**: Untuk kantor kecil atau gedung tunggal
- **100-200 meter**: Untuk kantor menengah atau kompleks kantor
- **200-500 meter**: Untuk area kantor yang luas atau kawasan industri
- **> 500 meter**: Tidak disarankan, terlalu luas dan kurang akurat

**Rekomendasi:** Gunakan radius **100-200 meter** untuk sebagian besar kasus.

### 2. **Akurasi Koordinat**

- Gunakan koordinat **pusat gedung kantor** atau **pintu masuk utama**
- Pastikan koordinat akurat dengan menggunakan Google Maps
- Hindari koordinat yang terlalu jauh dari lokasi sebenarnya

### 3. **Testing**

Setelah mengatur radius, **test** dengan:
1. Login sebagai karyawan
2. Coba check-in dari lokasi yang berbeda:
   - Dari dalam kantor (harus berhasil)
   - Dari luar kantor tapi masih dalam radius (harus berhasil)
   - Dari luar radius (harus gagal dengan pesan error)

### 4. **Koordinat Format**

- Latitude: **-90 sampai +90** (negatif untuk belahan bumi selatan)
- Longitude: **-180 sampai +180** (negatif untuk belahan bumi barat)
- Indonesia: Latitude negatif, Longitude positif

**Contoh untuk kota-kota di Indonesia:**
- Jakarta: `-6.2088, 106.8456`
- Bandung: `-6.9175, 107.6191`
- Surabaya: `-7.2575, 112.7521`
- Yogyakarta: `-7.7956, 110.3695`
- Medan: `3.5952, 98.6722`

---

## 🔧 Troubleshooting

### Masalah: Presensi selalu ditolak meskipun di kantor

**Kemungkinan penyebab:**
1. Koordinat kantor salah
2. Radius terlalu kecil
3. GPS smartphone tidak akurat

**Solusi:**
1. Verifikasi koordinat dengan Google Maps
2. Perbesar radius (misalnya dari 100m menjadi 150m)
3. Pastikan GPS smartphone aktif dan akurat
4. Cek apakah ada gedung tinggi yang menghalangi sinyal GPS

### Masalah: Presensi diterima meskipun di luar kantor

**Kemungkinan penyebab:**
1. Radius terlalu besar
2. Koordinat kantor tidak tepat

**Solusi:**
1. Perkecil radius (misalnya dari 200m menjadi 100m)
2. Perbaiki koordinat kantor agar lebih tepat

### Masalah: Perubahan konfigurasi tidak diterapkan

**Solusi:**
1. Pastikan sudah **restart aplikasi** setelah mengubah config
2. Pastikan tidak ada typo di file config
3. Cek apakah menggunakan environment variables dengan benar
4. Clear cache browser jika perlu

### Masalah: Error saat mengubah config

**Kemungkinan penyebab:**
1. Format angka salah (harus menggunakan titik, bukan koma)
2. Tipe data salah

**Solusi:**
- Pastikan format benar:
  ```python
  OFFICE_LATITUDE = -6.2088      # Benar (menggunakan titik)
  OFFICE_LATITUDE = -6,2088      # Salah (menggunakan koma)
  ```

---

## 📝 Contoh Konfigurasi

### Contoh 1: Kantor di Jakarta Pusat

```python
# Geolocation Settings
OFFICE_LATITUDE = -6.2088      # Koordinat Jakarta Pusat
OFFICE_LONGITUDE = 106.8456
GEO_RADIUS_METERS = 100        # Radius 100 meter
```

### Contoh 2: Kantor di Bandung (Area Luas)

```python
# Geolocation Settings
OFFICE_LATITUDE = -6.9175      # Koordinat Bandung
OFFICE_LONGITUDE = 107.6191
GEO_RADIUS_METERS = 200        # Radius 200 meter (area lebih luas)
```

### Contoh 3: Kantor di Surabaya (Gedung Kecil)

```python
# Geolocation Settings
OFFICE_LATITUDE = -7.2575      # Koordinat Surabaya
OFFICE_LONGITUDE = 112.7521
GEO_RADIUS_METERS = 75         # Radius 75 meter (gedung kecil)
```

### Contoh 4: Menggunakan Environment Variables

**File .env:**
```env
OFFICE_LATITUDE=-6.2088
OFFICE_LONGITUDE=106.8456
GEO_RADIUS_METERS=150
```

**File config.py:**
```python
# Geolocation Settings
OFFICE_LATITUDE = float(os.environ.get('OFFICE_LATITUDE', -6.2088))
OFFICE_LONGITUDE = float(os.environ.get('OFFICE_LONGITUDE', 106.8456))
GEO_RADIUS_METERS = int(os.environ.get('GEO_RADIUS_METERS', 100))
```

---

## ✅ Checklist Setelah Mengatur Radius

Setelah mengatur radius kantor, pastikan:

- [ ] Koordinat kantor sudah benar dan akurat
- [ ] Radius sudah disesuaikan dengan ukuran area kantor
- [ ] File config.py sudah disimpan
- [ ] Aplikasi sudah di-restart
- [ ] Sudah melakukan testing check-in dari berbagai lokasi
- [ ] Presensi berhasil dari dalam kantor
- [ ] Presensi ditolak dari luar radius

---

## 📞 Bantuan Tambahan

Jika masih mengalami masalah:

1. Cek dokumentasi di `documentation_flow/ATTENDANCE_FLOW.md`
2. Cek file `utils/geolocation.py` untuk detail implementasi
3. Cek log aplikasi untuk melihat error yang terjadi
4. Hubungi administrator sistem

---

**Selamat! Radius kantor Anda sudah dikonfigurasi dengan benar.** 🎉
