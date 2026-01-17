# Tutorial Login dengan Akun Karyawan

Panduan lengkap untuk login ke sistem presensi menggunakan akun karyawan.

---

## 📋 Daftar Isi

1. [Persiapan](#persiapan)
2. [Langkah-langkah Login](#langkah-langkah-login)
3. [Daftar Akun Karyawan yang Tersedia](#daftar-akun-karyawan-yang-tersedia)
4. [Troubleshooting](#troubleshooting)
5. [Fitur yang Dapat Diakses Setelah Login](#fitur-yang-dapat-diakses-setelah-login)

---

## 🚀 Persiapan

### 1. Pastikan Aplikasi Berjalan

Jalankan aplikasi dengan perintah berikut:

```bash
python app.py
```

Atau jika menggunakan PowerShell:

```powershell
python app.py
```

Aplikasi akan berjalan di: **http://localhost:5000** atau **http://127.0.0.1:5000**

### 2. Buka Browser

Buka browser web (Chrome, Firefox, Edge, dll) dan pastikan JavaScript diaktifkan.

---

## 📝 Langkah-langkah Login

### Langkah 1: Akses Halaman Login

1. Buka browser dan ketikkan alamat berikut di address bar:
   ```
   http://localhost:5000/auth/login
   ```
   
   Atau jika aplikasi berjalan di port lain, sesuaikan dengan port yang digunakan.

2. Tekan **Enter** untuk membuka halaman login.

### Langkah 2: Masukkan Kredensial Login

Di halaman login, Anda akan melihat form dengan 2 field:

1. **Username**
   - Klik pada field "Username"
   - Ketikkan username karyawan (contoh: `karyawan1`)

2. **Password**
   - Klik pada field "Password"
   - Ketikkan password karyawan (default: `karyawan123`)

**Contoh kredensial untuk login:**
- Username: `karyawan1`
- Password: `karyawan123`

### Langkah 3: Klik Tombol Login

1. Setelah mengisi username dan password, klik tombol **"Login"** yang berwarna biru di bagian bawah form.

2. Sistem akan memvalidasi kredensial Anda.

### Langkah 4: Berhasil Login

Jika kredensial benar, Anda akan:

1. Melihat pesan sukses: **"Login berhasil"** (warna hijau)
2. Otomatis diarahkan ke **Dashboard** karyawan
3. Dapat melihat menu dan fitur yang tersedia untuk role karyawan

---

## 👥 Daftar Akun Karyawan yang Tersedia

Berikut adalah daftar lengkap akun karyawan yang dapat digunakan untuk login:

### Karyawan Divisi IT (Atasan: Budi Santoso)

| No | Username | Password | Nama Lengkap | Posisi |
|----|----------|----------|--------------|--------|
| 1 | `karyawan1` | `karyawan123` | Ahmad Fauzi | Software Developer |
| 2 | `karyawan2` | `karyawan123` | Dewi Sartika | Frontend Developer |
| 3 | `karyawan3` | `karyawan123` | Rizki Pratama | Backend Developer |

### Karyawan Divisi HRD (Atasan: Siti Nurhaliza)

| No | Username | Password | Nama Lengkap | Posisi |
|----|----------|----------|--------------|--------|
| 4 | `karyawan4` | `karyawan123` | Indah Permata | HRD Staff |
| 5 | `karyawan5` | `karyawan123` | Bambang Wijaya | HRD Staff |

**⚠️ PENTING:** 
- Semua akun karyawan menggunakan password default yang sama: `karyawan123`
- **Sangat disarankan untuk mengganti password setelah login pertama kali** untuk keamanan akun Anda.

---

## 🔧 Troubleshooting

### Masalah: "Username atau password salah"

**Solusi:**
1. Pastikan Anda mengetikkan username dan password dengan benar (case-sensitive)
2. Periksa apakah ada spasi di awal atau akhir input
3. Gunakan salah satu akun dari daftar di atas
4. Pastikan password yang digunakan adalah: `karyawan123` (tanpa spasi)

### Masalah: "Akun Anda tidak aktif"

**Solusi:**
1. Hubungi administrator untuk mengaktifkan akun Anda
2. Pastikan akun karyawan sudah dibuat dengan benar di database

### Masalah: Halaman login tidak muncul / Error 404

**Solusi:**
1. Pastikan aplikasi sudah berjalan (cek terminal/command prompt)
2. Pastikan URL yang digunakan benar: `http://localhost:5000/auth/login`
3. Cek apakah port 5000 tidak digunakan oleh aplikasi lain
4. Restart aplikasi jika perlu

### Masalah: Tidak bisa mengakses setelah login

**Solusi:**
1. Clear cache browser (Ctrl + Shift + Delete)
2. Coba gunakan mode incognito/private
3. Pastikan cookies diaktifkan di browser
4. Coba logout dan login lagi

---

## 🎯 Fitur yang Dapat Diakses Setelah Login

Setelah berhasil login sebagai karyawan, Anda dapat mengakses fitur-fitur berikut:

### 1. **Dashboard**
   - URL: `http://localhost:5000/`
   - Menampilkan statistik presensi, notifikasi, dan informasi umum

### 2. **Presensi (Attendance)**
   - URL: `http://localhost:5000/attendance`
   - **Check In**: Mencatat waktu masuk kerja
   - **Check Out**: Mencatat waktu pulang kerja
   - **Riwayat Presensi**: Melihat history presensi Anda

### 3. **Pengajuan Cuti (Leave Request)**
   - URL: `http://localhost:5000/leave`
   - Membuat pengajuan cuti/izin
   - Melihat status pengajuan cuti
   - Melihat riwayat pengajuan

### 4. **Pengajuan Lembur (Overtime)**
   - URL: `http://localhost:5000/overtime`
   - Membuat pengajuan lembur
   - Melihat status pengajuan lembur
   - Melihat riwayat pengajuan

### 5. **Notifikasi**
   - URL: `http://localhost:5000/notification`
   - Melihat notifikasi dari sistem
   - Notifikasi persetujuan cuti/lembur
   - Notifikasi presensi

### 6. **Logout**
   - URL: `http://localhost:5000/auth/logout`
   - Keluar dari sistem dengan aman

---

## 📌 Tips Penting

1. **Keamanan Password:**
   - Ganti password default setelah login pertama kali
   - Gunakan password yang kuat (minimal 8 karakter, kombinasi huruf dan angka)
   - Jangan bagikan password Anda kepada siapapun

2. **Session:**
   - Session akan tetap aktif sampai Anda logout
   - Jika tidak digunakan, sebaiknya logout untuk keamanan
   - Session akan otomatis expired setelah beberapa waktu tidak aktif

3. **Presensi:**
   - Lakukan check in setiap hari kerja
   - Jangan lupa check out saat pulang
   - Sistem akan mencatat waktu dan lokasi presensi

4. **Pengajuan:**
   - Ajukan cuti/lembur dengan alasan yang jelas
   - Tunggu persetujuan dari atasan dan HRD
   - Cek notifikasi untuk update status pengajuan

---

## 🔐 Logout

Untuk logout dari sistem:

1. Klik menu **Logout** di bagian atas halaman (biasanya di pojok kanan)
2. Atau akses langsung: `http://localhost:5000/auth/logout`
3. Anda akan diarahkan kembali ke halaman login
4. Session akan dihapus dan Anda harus login lagi untuk mengakses sistem

---

## 📞 Bantuan

Jika mengalami masalah yang tidak dapat diselesaikan:

1. Cek dokumentasi lengkap di folder `documentation_flow/`
2. Hubungi administrator sistem
3. Cek log aplikasi untuk detail error

---

**Selamat menggunakan Sistem Presensi Karyawan!** 🎉
