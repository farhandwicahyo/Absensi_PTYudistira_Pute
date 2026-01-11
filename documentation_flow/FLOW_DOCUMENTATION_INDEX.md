# Indeks Dokumentasi Flow Sistem Presensi

Dokumen ini merupakan indeks untuk semua dokumentasi flow dalam sistem presensi karyawan.

---

## 📚 Daftar Dokumentasi

### 1. [AUTH_FLOW.md](./AUTH_FLOW.md)
**Flow Autentikasi dan Login**
- Flow login dan logout
- Session management
- Role-based access control
- Keamanan password
- Error handling

### 2. [ATTENDANCE_FLOW.md](./ATTENDANCE_FLOW.md)
**Flow Presensi (Check-in & Check-out)**
- Flow check-in dan check-out
- Validasi lokasi (geolocation)
- Validasi waktu
- Status presensi
- Riwayat presensi

### 3. [APPROVAL_WORKFLOW.md](./APPROVAL_WORKFLOW.md)
**Flow Approval Izin/Cuti/Sakit**
- Alur approval untuk cuti (2 tahap)
- Alur approval untuk izin dan sakit
- Notifikasi approval
- Validasi dan keamanan

### 4. [OVERTIME_FLOW.md](./OVERTIME_FLOW.md)
**Flow Pengajuan Lembur**
- Flow pengajuan lembur
- Flow approval lembur
- Perhitungan jam lembur
- Notifikasi lembur

### 5. [EMPLOYEE_MANAGEMENT_FLOW.md](./EMPLOYEE_MANAGEMENT_FLOW.md)
**Flow Manajemen Data Karyawan**
- Flow tambah karyawan
- Flow edit karyawan
- Flow hapus/nonaktifkan karyawan
- Flow import/export data

### 6. [NOTIFICATION_FLOW.md](./NOTIFICATION_FLOW.md)
**Flow Notifikasi Sistem**
- Jenis notifikasi
- Flow pembuatan notifikasi
- Flow menampilkan notifikasi
- Flow mark as read

### 7. [AUDIT_LOG_FLOW.md](./AUDIT_LOG_FLOW.md)
**Flow Audit Log**
- Flow pencatatan log
- Jenis aktivitas yang dicatat
- Flow melihat audit log
- Filter dan pencarian

---

## 🗺️ Peta Flow Utama

### Flow Autentikasi
```
Login → Session → Dashboard
  ↓
Logout → Clear Session → Login
```

### Flow Presensi
```
Check-in → Validasi Lokasi → Validasi Waktu → Simpan → Notifikasi
  ↓
Check-out → Validasi Lokasi → Update Status → Simpan → Notifikasi
```

### Flow Pengajuan Izin/Cuti/Sakit
```
Karyawan Ajukan → Notifikasi Atasan → Atasan Approve → Notifikasi HRD → HRD Approve → Notifikasi Karyawan
```

### Flow Pengajuan Lembur
```
Karyawan Ajukan → Notifikasi Atasan → Atasan Approve → Notifikasi HRD → HRD Approve → Notifikasi Karyawan
```

### Flow Manajemen Karyawan
```
Tambah → Validasi → Simpan → Audit Log
Edit → Validasi → Update → Audit Log
Hapus → Soft Delete → Update Status → Audit Log
Import → Validasi → Batch Create → Audit Log
Export → Query → Generate CSV → Download
```

### Flow Notifikasi
```
Event → Create Notification → Save to DB → Fetch → Display → Mark as Read
```

### Flow Audit Log
```
Activity → Create Log → Save to DB → Admin View → Filter → Display
```

---

## 🔗 Hubungan Antar Flow

### 1. **Autentikasi → Semua Flow**
Semua flow memerlukan autentikasi terlebih dahulu (kecuali login).

### 2. **Presensi → Notifikasi → Audit Log**
- Presensi trigger notifikasi
- Presensi dicatat di audit log

### 3. **Pengajuan → Approval → Notifikasi → Audit Log**
- Pengajuan trigger notifikasi ke atasan
- Approval trigger notifikasi ke karyawan
- Semua dicatat di audit log

### 4. **Manajemen Karyawan → Audit Log**
Semua perubahan data karyawan dicatat di audit log.

---

## 📖 Cara Menggunakan Dokumentasi

1. **Untuk Developer Baru:**
   - Baca semua flow secara berurutan
   - Mulai dari AUTH_FLOW.md
   - Lanjut ke flow lainnya

2. **Untuk Debugging:**
   - Identifikasi flow yang bermasalah
   - Baca dokumentasi flow tersebut
   - Cek detail proses dan error handling

3. **Untuk Implementasi Fitur Baru:**
   - Pahami flow yang relevan
   - Ikuti pattern yang sudah ada
   - Update dokumentasi jika ada perubahan

4. **Untuk Testing:**
   - Gunakan skenario di setiap dokumentasi
   - Test semua path dalam flow
   - Verifikasi error handling

---

## 📝 Catatan

- Semua dokumentasi menggunakan format Markdown
- Setiap flow memiliki diagram dan contoh skenario
- Dokumentasi akan diperbarui jika ada perubahan flow
- Untuk pertanyaan, lihat dokumentasi flow yang relevan

---

*Dokumentasi ini dibuat untuk memudahkan pemahaman dan maintenance sistem.*
