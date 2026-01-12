# Mode Demo - Menjalankan Aplikasi Tanpa Database

Dokumen ini menjelaskan cara menjalankan aplikasi dalam mode demo untuk melihat tampilan UI tanpa perlu menghubungkan ke database.

---

## 🎯 Tujuan

Mode demo memungkinkan Anda untuk:
- ✅ Melihat semua tampilan UI tanpa database
- ✅ Test semua halaman dan fitur
- ✅ Melihat perbedaan tampilan per role
- ✅ Tidak perlu setup database terlebih dahulu

---

## 🚀 Cara Menjalankan

### Opsi 1: Menggunakan `app_demo.py` (Recommended)

```bash
python app_demo.py
```

Aplikasi akan berjalan di `http://localhost:5000`

### Opsi 2: Menggunakan Environment Variable

```bash
# Windows PowerShell
$env:DEMO_MODE="true"
python app.py

# Windows CMD
set DEMO_MODE=true
python app.py

# Linux/Mac
export DEMO_MODE=true
python app.py
```

---

## 🔑 Login

**Mode demo tidak memerlukan login yang valid!**

1. Buka `http://localhost:5000`
2. Anda akan otomatis login sebagai user demo
3. Atau akses langsung halaman manapun (akan auto-login)

**Default Role:** `karyawan`

---

## 👤 Mengubah Role untuk Melihat Tampilan Berbeda

Untuk melihat tampilan yang berbeda per role, gunakan URL berikut:

### Karyawan
```
http://localhost:5000/change-role?role=karyawan
```

### Atasan
```
http://localhost:5000/change-role?role=atasan
```

### HRD
```
http://localhost:5000/change-role?role=hrd
```

### Admin
```
http://localhost:5000/change-role?role=admin
```

Atau gunakan menu login dan pilih role di form (jika ada).

---

## 📋 Fitur yang Tersedia

### ✅ Bekerja (dengan Mock Data)
- Dashboard (semua role)
- Halaman Presensi
- Halaman Data Karyawan
- Halaman Izin/Cuti/Sakit
- Halaman Lembur
- Halaman Audit Log
- Notifikasi

### ⚠️ Fitur yang Tidak Bekerja (karena tidak ada database)
- Check-in/Check-out (hanya tampil pesan demo)
- Simpan data (hanya flash message)
- Approval (hanya flash message)
- Import/Export (hanya flash message)

---

## 📊 Mock Data

Aplikasi menggunakan mock data untuk menampilkan:
- **10 data karyawan** (dengan berbagai jabatan dan divisi)
- **10 data presensi** (dengan berbagai status)
- **5 data pengajuan izin/cuti/sakit**
- **5 data pengajuan lembur**
- **5 notifikasi**
- **20 audit log**

Semua data ini **tidak tersimpan** dan akan **reset** setiap kali reload.

---

## 🎨 Halaman yang Bisa Dilihat

### 1. Dashboard
- URL: `http://localhost:5000/`
- Menampilkan statistik sesuai role
- Notifikasi terbaru

### 2. Presensi
- URL: `http://localhost:5000/attendance/`
- Tampilan check-in/check-out
- Riwayat presensi

### 3. Data Karyawan (HRD/Admin)
- URL: `http://localhost:5000/employee/`
- Daftar karyawan
- Form tambah/edit
- Import/Export

### 4. Izin/Cuti/Sakit
- URL: `http://localhost:5000/leave/`
- Daftar pengajuan
- Form pengajuan
- Approval (demo)

### 5. Lembur
- URL: `http://localhost:5000/overtime/`
- Daftar pengajuan lembur
- Form pengajuan
- Approval (demo)

### 6. Audit Log (Admin)
- URL: `http://localhost:5000/audit/`
- Daftar audit log
- Filter tanggal dan aktivitas

---

## 🔄 Perbedaan dengan Mode Normal

| Aspek | Demo Mode | Normal Mode |
|-------|-----------|-------------|
| Database | ❌ Tidak perlu | ✅ Wajib |
| Data | Mock data | Data real |
| Simpan Data | ❌ Tidak tersimpan | ✅ Tersimpan |
| Login | Auto login | Validasi password |
| Check-in/out | Pesan demo | Validasi GPS & waktu |
| Approval | Pesan demo | Update database |

---

## 💡 Tips

1. **Ganti Role**: Gunakan `/change-role?role=admin` untuk melihat tampilan admin
2. **Refresh**: Data mock akan berubah setiap refresh (untuk variasi)
3. **Test UI**: Semua tombol dan form bisa diklik, tapi tidak akan menyimpan data
4. **Responsive**: Test di berbagai ukuran layar untuk melihat responsive design

---

## ⚠️ Catatan Penting

1. **Data tidak tersimpan**: Semua perubahan tidak akan tersimpan
2. **Tidak ada validasi real**: Validasi hanya untuk demo
3. **Tidak ada koneksi database**: Semua query diganti dengan mock data
4. **Hanya untuk preview**: Gunakan untuk melihat UI, bukan untuk testing fungsional

---

## 🐛 Troubleshooting

### Error: Port sudah digunakan
```bash
# Ganti port di app_demo.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Template tidak ditemukan
Pastikan struktur folder `templates/` sudah benar.

### CSS/JS tidak load
Pastikan koneksi internet aktif (untuk CDN Tailwind/Flowbite).

---

## 📝 Contoh Penggunaan

### 1. Melihat Tampilan Karyawan
```bash
python app_demo.py
# Buka: http://localhost:5000
# Role default: karyawan
```

### 2. Melihat Tampilan Admin
```bash
python app_demo.py
# Buka: http://localhost:5000/change-role?role=admin
# Refresh halaman untuk melihat perubahan
```

### 3. Test Semua Halaman
1. Dashboard: `http://localhost:5000/`
2. Presensi: `http://localhost:5000/attendance/`
3. Data Karyawan: `http://localhost:5000/employee/` (ganti role ke hrd/admin)
4. Izin/Cuti: `http://localhost:5000/leave/`
5. Lembur: `http://localhost:5000/overtime/`
6. Audit Log: `http://localhost:5000/audit/` (ganti role ke admin)

---

## 🎯 Next Steps

Setelah puas melihat tampilan, untuk menjalankan aplikasi dengan database:

1. Setup SQL Server
2. Konfigurasi `config.py`
3. Jalankan `python init_db.py`
4. Jalankan `python app.py` (bukan `app_demo.py`)

---

*Mode demo ini dibuat untuk memudahkan preview UI sebelum setup database.*
