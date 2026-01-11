# Dokumentasi Folder Utils

Folder `utils` berisi **utility functions** dan **helper classes** yang digunakan di seluruh aplikasi. File-file di sini berisi fungsi-fungsi yang dapat digunakan kembali (reusable) untuk berbagai keperluan seperti autentikasi, logging, validasi, dan notifikasi.

---

## 📁 Struktur Folder Utils

```
utils/
├── __init__.py              # File inisialisasi package
├── audit_logger.py          # Utility untuk audit logging
├── decorators.py             # Decorators untuk autentikasi & autorisasi
├── geolocation.py            # Utility untuk validasi lokasi GPS
├── device_info.py            # Utility untuk mendapatkan info perangkat
└── notification_helper.py    # Helper untuk membuat notifikasi
```

---

## 📄 Penjelasan Detail Setiap File

### 1. `audit_logger.py` - Audit Logging System

**Fungsi Utama:**
Mencatat semua aktivitas penting di sistem ke dalam audit log untuk keamanan dan transparansi.

**Class & Methods:**

#### `AuditLogger` (Class)
Class utama untuk logging aktivitas sistem.

**Methods:**

1. **`log(user_id, username, activity, action, table_name, record_id, details)`**
   - **Fungsi**: Mencatat aktivitas umum ke audit log
   - **Parameter**:
     - `user_id`: ID user yang melakukan aktivitas
     - `username`: Username user
     - `activity`: Jenis aktivitas (login, presensi, data_change, dll)
     - `action`: Aksi yang dilakukan (create, update, delete, login_success, dll)
     - `table_name`: Nama tabel yang terpengaruh (opsional)
     - `record_id`: ID record yang terpengaruh (opsional)
     - `details`: Detail tambahan dalam format JSON/text (opsional)
   - **Return**: Tidak ada (void)
   - **Contoh Penggunaan**:
     ```python
     AuditLogger.log(1, 'admin', 'data_change', 'update', 'employees', 5, 'Updated salary')
     ```

2. **`log_login(user_id, username, success=True)`**
   - **Fungsi**: Mencatat aktivitas login (berhasil/gagal)
   - **Parameter**:
     - `user_id`: ID user (None jika login gagal)
     - `username`: Username yang mencoba login
     - `success`: True jika login berhasil, False jika gagal
   - **Contoh Penggunaan**:
     ```python
     AuditLogger.log_login(1, 'admin', success=True)
     AuditLogger.log_login(None, 'hacker', success=False)
     ```

3. **`log_logout(user_id, username)`**
   - **Fungsi**: Mencatat aktivitas logout
   - **Parameter**:
     - `user_id`: ID user yang logout
     - `username`: Username user
   - **Contoh Penggunaan**:
     ```python
     AuditLogger.log_logout(1, 'admin')
     ```

4. **`log_presensi(user_id, username, action, attendance_id, details)`**
   - **Fungsi**: Mencatat aktivitas presensi (check-in/check-out)
   - **Parameter**:
     - `user_id`: ID user
     - `username`: Username
     - `action`: 'check_in' atau 'check_out'
     - `attendance_id`: ID record presensi
     - `details`: Detail tambahan (misalnya koordinat GPS)
   - **Contoh Penggunaan**:
     ```python
     AuditLogger.log_presensi(1, 'karyawan1', 'check_in', 10, 'Location: -6.2088, 106.8456')
     ```

5. **`log_data_change(user_id, username, action, table_name, record_id, details)`**
   - **Fungsi**: Mencatat perubahan data (create, update, delete)
   - **Parameter**:
     - `user_id`: ID user yang melakukan perubahan
     - `username`: Username
     - `action`: 'create', 'update', atau 'delete'
     - `table_name`: Nama tabel (employees, leave_requests, dll)
     - `record_id`: ID record yang diubah
     - `details`: Detail perubahan
   - **Contoh Penggunaan**:
     ```python
     AuditLogger.log_data_change(1, 'hrd', 'update', 'employees', 5, 'Updated employee salary')
     ```

**Informasi yang Dicatat:**
- User ID dan username
- Aktivitas dan aksi
- Tabel dan record ID (jika ada)
- IP Address
- User Agent (browser & OS)
- Timestamp otomatis
- Detail tambahan

**Digunakan di:**
- `controllers/auth_controller.py` - Log login/logout
- `controllers/attendance_controller.py` - Log presensi
- `controllers/employee_controller.py` - Log perubahan data karyawan
- `controllers/leave_controller.py` - Log pengajuan izin/cuti
- `controllers/overtime_controller.py` - Log pengajuan lembur

---

### 2. `decorators.py` - Authentication & Authorization Decorators

**Fungsi Utama:**
Menyediakan decorators untuk melindungi route/rute agar hanya bisa diakses oleh user yang sudah login atau memiliki role tertentu.

**Decorators:**

1. **`@login_required`**
   - **Fungsi**: Memastikan user sudah login sebelum mengakses route
   - **Cara Kerja**:
     - Mengecek apakah `user_id` ada di session
     - Jika tidak ada, redirect ke halaman login dengan pesan warning
     - Jika ada, izinkan akses ke route
   - **Contoh Penggunaan**:
     ```python
     @attendance_bp.route('/')
     @login_required
     def index():
         return render_template('attendance/index.html')
     ```

2. **`@role_required(*roles)`**
   - **Fungsi**: Memastikan user memiliki salah satu role yang diizinkan
   - **Parameter**: 
     - `*roles`: List role yang diizinkan (admin, hrd, atasan, karyawan)
   - **Cara Kerja**:
     - Mengecek apakah user sudah login
     - Mengecek apakah role user ada dalam list role yang diizinkan
     - Jika tidak, redirect ke dashboard dengan pesan error
   - **Contoh Penggunaan**:
     ```python
     @employee_bp.route('/')
     @role_required('admin', 'hrd')
     def index():
         return render_template('employee/index.html')
     ```

3. **`@admin_required`**
   - **Fungsi**: Memastikan user adalah admin
   - **Cara Kerja**: Memanggil `@role_required('admin')`
   - **Contoh Penggunaan**:
     ```python
     @audit_bp.route('/')
     @admin_required
     def index():
         return render_template('audit/index.html')
     ```

4. **`@hrd_required`**
   - **Fungsi**: Memastikan user adalah HRD atau admin
   - **Cara Kerja**: Memanggil `@role_required('admin', 'hrd')`
   - **Contoh Penggunaan**:
     ```python
     @employee_bp.route('/create')
     @hrd_required
     def create():
         return render_template('employee/create.html')
     ```

5. **`@supervisor_required`**
   - **Fungsi**: Memastikan user adalah atasan, HRD, atau admin
   - **Cara Kerja**: Memanggil `@role_required('admin', 'hrd', 'atasan')`
   - **Contoh Penggunaan**:
     ```python
     @leave_bp.route('/<int:leave_id>/approve')
     @supervisor_required
     def approve(leave_id):
         # Logic approval
     ```

**Keuntungan Menggunakan Decorators:**
- **DRY (Don't Repeat Yourself)**: Tidak perlu menulis kode pengecekan di setiap route
- **Konsistensi**: Semua route menggunakan logika yang sama
- **Keamanan**: Memastikan tidak ada route yang terlewat dari pengecekan
- **Mudah dirawat**: Jika ada perubahan logika, cukup edit di satu tempat

**Digunakan di:**
- Semua controller untuk melindungi route

---

### 3. `geolocation.py` - GPS Location Validation

**Fungsi Utama:**
Validasi apakah lokasi user berada dalam radius yang diizinkan untuk presensi (geofencing).

**Functions:**

1. **`calculate_distance(lat1, lon1, lat2, lon2)`**
   - **Fungsi**: Menghitung jarak antara dua koordinat GPS menggunakan formula Haversine
   - **Parameter**:
     - `lat1, lon1`: Koordinat pertama (latitude, longitude)
     - `lat2, lon2`: Koordinat kedua (latitude, longitude)
   - **Return**: Jarak dalam meter (float)
   - **Formula**: Menggunakan Haversine formula untuk menghitung jarak di permukaan bumi
   - **Contoh Penggunaan**:
     ```python
     distance = calculate_distance(-6.2088, 106.8456, -6.2090, 106.8458)
     # Hasil: ~22.2 meter
     ```

2. **`validate_location(latitude, longitude)`**
   - **Fungsi**: Validasi apakah lokasi user berada dalam radius kantor
   - **Parameter**:
     - `latitude`: Latitude lokasi user
     - `longitude`: Longitude lokasi user
   - **Return**: Tuple `(is_valid, distance_in_meters)`
     - `is_valid`: Boolean, True jika dalam radius, False jika di luar
     - `distance_in_meters`: Jarak dari lokasi kantor dalam meter
   - **Cara Kerja**:
     1. Mengambil koordinat kantor dari `Config.OFFICE_LATITUDE` dan `Config.OFFICE_LONGITUDE`
     2. Menghitung jarak menggunakan `calculate_distance()`
     3. Membandingkan dengan `Config.GEO_RADIUS_METERS`
     4. Return True jika jarak <= radius, False jika sebaliknya
   - **Contoh Penggunaan**:
     ```python
     is_valid, distance = validate_location(-6.2088, 106.8456)
     if is_valid:
         print(f"Lokasi valid, jarak: {distance:.2f} meter")
     else:
         print(f"Lokasi di luar radius, jarak: {distance:.2f} meter")
     ```

**Konfigurasi:**
- Koordinat kantor: `Config.OFFICE_LATITUDE` dan `Config.OFFICE_LONGITUDE`
- Radius: `Config.GEO_RADIUS_METERS` (default: 100 meter)

**Digunakan di:**
- `controllers/attendance_controller.py` - Validasi lokasi saat check-in/check-out

---

### 4. `device_info.py` - Device Information Detection

**Fungsi Utama:**
Mendeteksi informasi perangkat user dari HTTP request headers (browser, OS, IP address).

**Functions:**

1. **`get_browser_info()`**
   - **Fungsi**: Mendeteksi browser dari User-Agent header
   - **Return**: String nama browser (Chrome, Firefox, Safari, Edge, Opera, atau Unknown)
   - **Cara Kerja**:
     - Membaca `User-Agent` header dari request
     - Mencocokkan dengan pola browser tertentu
   - **Contoh Penggunaan**:
     ```python
     browser = get_browser_info()
     # Hasil: "Chrome", "Firefox", "Safari", dll
     ```

2. **`get_os_info()`**
   - **Fungsi**: Mendeteksi sistem operasi dari User-Agent header
   - **Return**: String nama OS (Windows, macOS, Linux, Android, iOS, atau Unknown)
   - **Cara Kerja**:
     - Membaca `User-Agent` header dari request
     - Mencocokkan dengan pola OS tertentu
   - **Contoh Penggunaan**:
     ```python
     os = get_os_info()
     # Hasil: "Windows", "macOS", "Linux", dll
     ```

3. **`get_device_info()`**
   - **Fungsi**: Mendapatkan semua informasi perangkat sekaligus
   - **Return**: Dictionary dengan keys:
     - `browser`: Nama browser
     - `os`: Nama sistem operasi
     - `ip_address`: IP address user
     - `user_agent`: Full User-Agent string
   - **Contoh Penggunaan**:
     ```python
     device_info = get_device_info()
     # Hasil: {
     #   'browser': 'Chrome',
     #   'os': 'Windows',
     #   'ip_address': '192.168.1.1',
     #   'user_agent': 'Mozilla/5.0...'
     # }
     ```

**Kegunaan:**
- Mencatat informasi perangkat untuk audit log
- Mencegah manipulasi presensi (dengan mencatat browser dan OS)
- Analisis penggunaan sistem (browser/OS apa yang paling banyak digunakan)

**Digunakan di:**
- `controllers/auth_controller.py` - Mencatat info perangkat saat login
- `controllers/attendance_controller.py` - Mencatat info perangkat saat presensi

---

### 5. `notification_helper.py` - Notification System Helper

**Fungsi Utama:**
Helper class untuk membuat notifikasi sistem dengan mudah dan konsisten.

**Class & Methods:**

#### `NotificationHelper` (Class)
Class helper untuk membuat berbagai jenis notifikasi.

**Methods:**

1. **`create_notification(user_id, title, message, notification_type, related_id=None)`**
   - **Fungsi**: Membuat notifikasi umum
   - **Parameter**:
     - `user_id`: ID user yang akan menerima notifikasi
     - `title`: Judul notifikasi
     - `message`: Pesan notifikasi
     - `notification_type`: Jenis notifikasi (presensi, leave, overtime, dll)
     - `related_id`: ID record terkait (opsional)
   - **Return**: Object Notification atau None jika error
   - **Contoh Penggunaan**:
     ```python
     NotificationHelper.create_notification(
         1, 
         'Pesan Penting', 
         'Ada pembaruan sistem', 
         'system',
         related_id=None
     )
     ```

2. **`notify_presensi_success(user_id, attendance_id)`**
   - **Fungsi**: Notifikasi presensi berhasil
   - **Parameter**:
     - `user_id`: ID user
     - `attendance_id`: ID presensi
   - **Contoh Penggunaan**:
     ```python
     NotificationHelper.notify_presensi_success(1, 10)
     ```

3. **`notify_presensi_failed(user_id, reason)`**
   - **Fungsi**: Notifikasi presensi gagal
   - **Parameter**:
     - `user_id`: ID user
     - `reason`: Alasan kegagalan
   - **Contoh Penggunaan**:
     ```python
     NotificationHelper.notify_presensi_failed(1, 'Lokasi di luar radius')
     ```

4. **`notify_leave_submitted(user_id, leave_request_id, leave_type)`**
   - **Fungsi**: Notifikasi pengajuan izin/cuti/sakit dikirim
   - **Parameter**:
     - `user_id`: ID user yang mengajukan
     - `leave_request_id`: ID pengajuan
     - `leave_type`: Jenis (izin, cuti, sakit)
   - **Contoh Penggunaan**:
     ```python
     NotificationHelper.notify_leave_submitted(1, 5, 'cuti')
     ```

5. **`notify_leave_approval(user_id, leave_request_id, approved, leave_type)`**
   - **Fungsi**: Notifikasi persetujuan/tolakan izin/cuti/sakit
   - **Parameter**:
     - `user_id`: ID user
     - `leave_request_id`: ID pengajuan
     - `approved`: True jika disetujui, False jika ditolak
     - `leave_type`: Jenis (izin, cuti, sakit)
   - **Contoh Penggunaan**:
     ```python
     NotificationHelper.notify_leave_approval(1, 5, True, 'cuti')
     ```

6. **`notify_overtime_submitted(user_id, overtime_id)`**
   - **Fungsi**: Notifikasi pengajuan lembur dikirim
   - **Parameter**:
     - `user_id`: ID user
     - `overtime_id`: ID pengajuan lembur
   - **Contoh Penggunaan**:
     ```python
     NotificationHelper.notify_overtime_submitted(1, 3)
     ```

7. **`notify_overtime_approval(user_id, overtime_id, approved)`**
   - **Fungsi**: Notifikasi persetujuan/tolakan lembur
   - **Parameter**:
     - `user_id`: ID user
     - `overtime_id`: ID pengajuan
     - `approved`: True jika disetujui, False jika ditolak
   - **Contoh Penggunaan**:
     ```python
     NotificationHelper.notify_overtime_approval(1, 3, True)
     ```

**Keuntungan:**
- Konsistensi: Semua notifikasi menggunakan format yang sama
- Mudah digunakan: Cukup panggil method yang sesuai
- Mudah dirawat: Jika format notifikasi berubah, cukup edit di satu tempat

**Digunakan di:**
- `controllers/attendance_controller.py` - Notifikasi presensi
- `controllers/leave_controller.py` - Notifikasi pengajuan izin/cuti
- `controllers/overtime_controller.py` - Notifikasi pengajuan lembur

---

## 🔄 Alur Penggunaan Utils dalam Aplikasi

### Contoh: Proses Check-in Presensi

```python
# 1. Decorator memastikan user sudah login
@attendance_bp.route('/check-in', methods=['POST'])
@login_required  # ← dari decorators.py
def check_in():
    # 2. Validasi lokasi GPS
    is_valid, distance = validate_location(latitude, longitude)  # ← dari geolocation.py
    if not is_valid:
        return jsonify({'error': 'Lokasi di luar radius'})
    
    # 3. Dapatkan info perangkat
    device_info = get_device_info()  # ← dari device_info.py
    
    # 4. Simpan presensi
    attendance = Attendance(...)
    db.session.commit()
    
    # 5. Log ke audit log
    AuditLogger.log_presensi(...)  # ← dari audit_logger.py
    
    # 6. Buat notifikasi
    NotificationHelper.notify_presensi_success(...)  # ← dari notification_helper.py
    
    return jsonify({'success': True})
```

---

## 📊 Ringkasan

| File | Fungsi Utama | Digunakan Untuk |
|------|-------------|-----------------|
| `audit_logger.py` | Mencatat aktivitas sistem | Keamanan, transparansi, audit |
| `decorators.py` | Melindungi route | Autentikasi & autorisasi |
| `geolocation.py` | Validasi lokasi GPS | Presensi berbasis lokasi |
| `device_info.py` | Deteksi info perangkat | Audit log, keamanan |
| `notification_helper.py` | Membuat notifikasi | Komunikasi dengan user |

---

## 💡 Best Practices

1. **Jangan mengubah logika di utils tanpa pertimbangan** - Karena digunakan di banyak tempat
2. **Gunakan method yang sudah ada** - Jangan membuat fungsi baru jika sudah ada yang serupa
3. **Handle error dengan baik** - Utils harus robust dan tidak crash aplikasi
4. **Dokumentasikan perubahan** - Jika menambah method baru, dokumentasikan dengan baik

---

## 🔧 Maintenance

Jika perlu menambah fungsi baru:
1. Tentukan apakah fungsi tersebut reusable (bisa digunakan di banyak tempat)
2. Jika ya, tambahkan ke utils
3. Jika tidak, letakkan di controller yang relevan
4. Dokumentasikan dengan docstring yang jelas
