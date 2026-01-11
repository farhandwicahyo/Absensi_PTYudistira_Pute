# Perbedaan Tampilan Berdasarkan Role

Dokumen ini menjelaskan perbedaan tampilan dan fitur yang tersedia untuk setiap role (Admin, HRD, Atasan, Karyawan) dalam sistem presensi.

---

## 📊 Ringkasan Perbedaan

| Fitur | Karyawan | Atasan | HRD | Admin |
|-------|----------|--------|-----|-------|
| **Dashboard** | Presensi hari ini, Pengajuan pending | Bawahan, Pengajuan pending | Total karyawan, Presensi hari ini, Pengajuan | Total karyawan, Presensi hari ini, Pengajuan |
| **Menu Sidebar** | Dashboard, Presensi, Izin/Cuti, Lembur | Dashboard, Presensi, Izin/Cuti, Lembur | + Data Karyawan | + Data Karyawan, + Audit Log |
| **Presensi** | Check-in/out sendiri | Lihat riwayat bawahan | Lihat semua presensi | Lihat semua presensi |
| **Data Karyawan** | ❌ Tidak bisa akses | ❌ Tidak bisa akses | ✅ Full access | ✅ Full access |
| **Izin/Cuti/Sakit** | Ajukan, lihat sendiri | Approve/reject bawahan | Approve/reject semua | Approve/reject semua |
| **Lembur** | Ajukan, lihat sendiri | Approve/reject bawahan | Approve/reject semua | Approve/reject semua |
| **Audit Log** | ❌ Tidak bisa akses | ❌ Tidak bisa akses | ❌ Tidak bisa akses | ✅ Full access |

---

## 👤 1. KARYAWAN

### Dashboard
- **3 Card Statistik:**
  - Presensi Hari Ini (Sudah/Belum)
  - Pengajuan Pending (izin/cuti/sakit)
  - Lembur Pending

### Menu Sidebar
- ✅ Dashboard
- ✅ Presensi
- ✅ Izin/Cuti/Sakit
- ✅ Lembur
- ❌ Data Karyawan (tidak muncul)
- ❌ Audit Log (tidak muncul)

### Presensi
- **Halaman Presensi:**
  - Tombol Check-in dan Check-out aktif
  - Riwayat presensi sendiri (10 terakhir)
  - Kolom: Tanggal, Check In, Check Out, Status
  
- **Riwayat Presensi:**
  - Hanya menampilkan presensi sendiri
  - Filter tanggal
  - Kolom: Tanggal, Check In, Check Out, Status, Keterangan

### Izin/Cuti/Sakit
- **Tombol "Ajukan"** muncul di halaman index
- Hanya melihat pengajuan sendiri
- Tidak bisa approve/reject

### Lembur
- **Tombol "Ajukan"** muncul di halaman index
- Hanya melihat pengajuan sendiri
- Tidak bisa approve/reject

### Badge Role
- Badge hijau dengan teks "Karyawan" di navbar

---

## 👔 2. ATASAN (Supervisor)

### Dashboard
- **3 Card Statistik:**
  - Jumlah Bawahan
  - Pengajuan Pending (dari bawahan)
  - Lembur Pending (dari bawahan)

### Menu Sidebar
- ✅ Dashboard
- ✅ Presensi
- ✅ Izin/Cuti/Sakit
- ✅ Lembur
- ❌ Data Karyawan (tidak muncul)
- ❌ Audit Log (tidak muncul)

### Presensi
- **Halaman Presensi:**
  - Info box: "Sebagai Atasan, Anda dapat melihat riwayat presensi..."
  - Tidak ada tombol check-in/out
  - Riwayat presensi bawahan (10 terakhir)
  - Kolom: Tanggal, **Karyawan**, Check In, Check Out, Status
  
- **Riwayat Presensi:**
  - Menampilkan presensi bawahan saja
  - Filter tanggal
  - Kolom: Tanggal, **Karyawan**, Check In, Check Out, Status, Keterangan

### Izin/Cuti/Sakit
- **Tombol "Ajukan"** TIDAK muncul
- Melihat pengajuan dari bawahan
- **Tombol Approve/Reject** muncul untuk pengajuan yang menunggu
- Bisa approve/reject pengajuan bawahan

### Lembur
- **Tombol "Ajukan"** TIDAK muncul
- Melihat pengajuan dari bawahan
- **Tombol Approve/Reject** muncul untuk pengajuan yang menunggu
- Bisa approve/reject pengajuan bawahan

### Badge Role
- Badge ungu dengan teks "Atasan" di navbar

---

## 👥 3. HRD

### Dashboard
- **4 Card Statistik:**
  - Total Karyawan (aktif)
  - Presensi Hari Ini (semua karyawan)
  - Pengajuan Pending (semua)
  - Lembur Pending (semua)

### Menu Sidebar
- ✅ Dashboard
- ✅ Presensi
- ✅ **Data Karyawan** (muncul)
- ✅ Izin/Cuti/Sakit
- ✅ Lembur
- ❌ Audit Log (tidak muncul)

### Presensi
- **Halaman Presensi:**
  - Info box: "Sebagai HRD, Anda dapat melihat riwayat presensi..."
  - Tidak ada tombol check-in/out
  - Riwayat presensi semua karyawan (10 terakhir)
  - Kolom: Tanggal, **Karyawan**, Check In, Check Out, Status
  
- **Riwayat Presensi:**
  - Menampilkan presensi semua karyawan
  - Filter tanggal
  - Kolom: Tanggal, **Karyawan**, Check In, Check Out, Status, Keterangan

### Data Karyawan
- ✅ Full access (CRUD)
- Import/Export CSV
- Tambah, Edit, Hapus (nonaktifkan) karyawan

### Izin/Cuti/Sakit
- **Tombol "Ajukan"** TIDAK muncul
- Melihat semua pengajuan
- **Tombol Approve/Reject** muncul untuk pengajuan yang menunggu
- Bisa approve/reject semua pengajuan

### Lembur
- **Tombol "Ajukan"** TIDAK muncul
- Melihat semua pengajuan
- **Tombol Approve/Reject** muncul untuk pengajuan yang menunggu
- Bisa approve/reject semua pengajuan

### Badge Role
- Badge biru dengan teks "HRD" di navbar

---

## 🔐 4. ADMIN

### Dashboard
- **4 Card Statistik:**
  - Total Karyawan (aktif)
  - Presensi Hari Ini (semua karyawan)
  - Pengajuan Pending (semua)
  - Lembur Pending (semua)

### Menu Sidebar
- ✅ Dashboard
- ✅ Presensi
- ✅ **Data Karyawan** (muncul)
- ✅ Izin/Cuti/Sakit
- ✅ Lembur
- ✅ **Audit Log** (muncul)

### Presensi
- **Halaman Presensi:**
  - Info box: "Sebagai Admin, Anda dapat melihat riwayat presensi..."
  - Tidak ada tombol check-in/out
  - Riwayat presensi semua karyawan (10 terakhir)
  - Kolom: Tanggal, **Karyawan**, Check In, Check Out, Status
  
- **Riwayat Presensi:**
  - Menampilkan presensi semua karyawan
  - Filter tanggal
  - Kolom: Tanggal, **Karyawan**, Check In, Check Out, Status, Keterangan

### Data Karyawan
- ✅ Full access (CRUD)
- Import/Export CSV
- Tambah, Edit, Hapus (nonaktifkan) karyawan

### Izin/Cuti/Sakit
- **Tombol "Ajukan"** TIDAK muncul
- Melihat semua pengajuan
- **Tombol Approve/Reject** muncul untuk pengajuan yang menunggu
- Bisa approve/reject semua pengajuan

### Lembur
- **Tombol "Ajukan"** TIDAK muncul
- Melihat semua pengajuan
- **Tombol Approve/Reject** muncul untuk pengajuan yang menunggu
- Bisa approve/reject semua pengajuan

### Audit Log
- ✅ Full access
- Melihat semua aktivitas sistem
- Filter berdasarkan tanggal dan aktivitas
- Informasi: Waktu, User, Aktivitas, Aksi, Tabel, IP Address

### Badge Role
- Badge merah dengan teks "Admin" di navbar

---

## 🎨 Perbedaan Visual

### Badge Role di Navbar
- **Admin**: Badge merah (`bg-red-100 text-red-700`)
- **HRD**: Badge biru (`bg-blue-100 text-blue-700`)
- **Atasan**: Badge ungu (`bg-purple-100 text-purple-700`)
- **Karyawan**: Badge hijau (`bg-green-100 text-green-700`)

### Welcome Message
- Setiap role memiliki pesan selamat datang yang berbeda
- Badge role ditampilkan di dashboard

### Info Box
- Admin/HRD/Atasan melihat info box di halaman presensi
- Karyawan tidak melihat info box (langsung ke fitur presensi)

---

## 🔒 Keamanan

Semua perbedaan tampilan ini juga dilindungi di level controller menggunakan decorators:

- `@login_required` - Semua halaman memerlukan login
- `@hrd_required` - Hanya HRD dan Admin bisa akses Data Karyawan
- `@admin_required` - Hanya Admin bisa akses Audit Log
- `@supervisor_required` - Atasan, HRD, dan Admin bisa approve/reject

---

## 📝 Catatan

1. **Presensi Check-in/out** hanya bisa dilakukan oleh **Karyawan**
2. **Data Karyawan** hanya bisa diakses oleh **HRD** dan **Admin**
3. **Audit Log** hanya bisa diakses oleh **Admin**
4. **Approval** bisa dilakukan oleh **Atasan**, **HRD**, dan **Admin** sesuai dengan hierarki
5. Semua role bisa melihat **notifikasi** mereka sendiri

---

## 🔄 Alur Approval

### Izin/Cuti/Sakit
1. **Karyawan** mengajukan
2. **Atasan** approve/reject (jika ada)
3. **HRD/Admin** approve/reject (final)

### Lembur
1. **Karyawan** mengajukan
2. **Atasan** approve/reject (jika ada)
3. **HRD/Admin** approve/reject (final)

---

*Dokumen ini akan diperbarui jika ada perubahan fitur atau role baru.*
