# Flow Presensi (Check-in & Check-out)

Dokumen ini menjelaskan alur lengkap untuk presensi masuk (check-in) dan presensi pulang (check-out) dalam sistem presensi karyawan.

---

## 📋 Daftar Isi

1. [Flow Check-in](#flow-check-in)
2. [Flow Check-out](#flow-check-out)
3. [Validasi Lokasi (Geolocation)](#validasi-lokasi-geolocation)
4. [Validasi Waktu](#validasi-waktu)
5. [Status Presensi](#status-presensi)
6. [Riwayat Presensi](#riwayat-presensi)
7. [Error Handling](#error-handling)

---

## ✅ Flow Check-in

### Alur Lengkap

```
Karyawan Klik Tombol "Check In"
    ↓
Request Permission Geolocation (Browser)
    ↓
Dapatkan Koordinat GPS (latitude, longitude)
    ↓
Kirim Request ke Server (POST /attendance/check-in)
    ↓
Validasi: Employee ID ada?
    ↓
Cek: Sudah Check-in Hari Ini?
    ↓
Validasi: Lokasi dalam Radius?
    ↓
Deteksi Info Perangkat (Browser, OS, IP)
    ↓
Tentukan Status (Hadir/Terlambat)
    ↓
Simpan ke Database
    ↓
Log Audit
    ↓
Buat Notifikasi
    ↓
Return Success Response
    ↓
Reload Halaman
```

### Detail Proses

#### 1. **Request Geolocation (Frontend)**
```javascript
navigator.geolocation.getCurrentPosition(
    position => {
        const location = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
        };
        // Kirim ke server
    },
    error => {
        // Handle error
    }
);
```

#### 2. **Validasi Employee ID**
```python
employee_id = session.get('employee_id')
if not employee_id:
    return jsonify({'success': False, 'message': 'Data karyawan tidak ditemukan'}), 400
```

#### 3. **Cek Duplikasi Check-in**
```python
today = date.today()
existing = Attendance.query.filter_by(
    employee_id=employee_id,
    attendance_date=today
).first()

if existing and existing.check_in_time:
    return jsonify({'success': False, 'message': 'Anda sudah melakukan check-in hari ini'}), 400
```

#### 4. **Validasi Lokasi**
```python
# Validasi koordinat GPS
is_valid, distance = validate_location(latitude, longitude)

if not is_valid:
    return jsonify({
        'success': False, 
        'message': f'Anda berada di luar radius kantor. Jarak: {distance:.0f}m'
    }), 400
```

**Validasi:**
- Menghitung jarak dari koordinat user ke koordinat kantor
- Menggunakan formula Haversine
- Radius default: 100 meter (dapat diubah di config)

#### 5. **Deteksi Info Perangkat**
```python
device_info = get_device_info()
# Returns: {
#   'browser': 'Chrome',
#   'os': 'Windows',
#   'ip_address': '192.168.1.1',
#   'user_agent': 'Mozilla/5.0...'
# }
```

#### 6. **Tentukan Status**
```python
now = datetime.utcnow()
check_in_time = now.time()
check_in_start = datetime.strptime(Config.CHECK_IN_START, '%H:%M').time()

# Jika check-in setelah jam mulai, status = terlambat
status = 'terlambat' if check_in_time > check_in_start else 'hadir'
```

**Konfigurasi:**
- `CHECK_IN_START`: Jam mulai check-in (default: 07:00)
- `CHECK_IN_END`: Jam akhir check-in (default: 09:00)

#### 7. **Simpan ke Database**
```python
attendance = Attendance(
    employee_id=employee_id,
    attendance_date=today,
    check_in_time=now,
    check_in_latitude=latitude,
    check_in_longitude=longitude,
    check_in_ip=device_info['ip_address'],
    check_in_browser=device_info['browser'],
    check_in_os=device_info['os'],
    status=status
)
db.session.add(attendance)
db.session.commit()
```

**Data yang Disimpan:**
- Employee ID
- Tanggal presensi
- Waktu check-in
- Koordinat GPS (latitude, longitude)
- IP Address
- Browser
- OS
- Status (hadir/terlambat)

#### 8. **Audit Logging**
```python
AuditLogger.log_presensi(
    user_id,
    username,
    'check_in',
    attendance.id,
    f'Location: {latitude}, {longitude}'
)
```

#### 9. **Notifikasi**
```python
NotificationHelper.notify_presensi_success(user_id, attendance.id)
```

---

## 🚪 Flow Check-out

### Alur Lengkap

```
Karyawan Klik Tombol "Check Out"
    ↓
Request Permission Geolocation (Browser)
    ↓
Dapatkan Koordinat GPS
    ↓
Kirim Request ke Server (POST /attendance/check-out)
    ↓
Validasi: Employee ID ada?
    ↓
Cek: Sudah Check-in Hari Ini?
    ↓
Cek: Sudah Check-out Hari Ini?
    ↓
Validasi: Lokasi dalam Radius?
    ↓
Deteksi Info Perangkat
    ↓
Cek: Pulang Cepat?
    ↓
Update Status (jika perlu)
    ↓
Update Database
    ↓
Log Audit
    ↓
Return Success Response
    ↓
Reload Halaman
```

### Detail Proses

#### 1. **Validasi Check-in**
```python
# Harus sudah check-in dulu
attendance = Attendance.query.filter_by(
    employee_id=employee_id,
    attendance_date=today
).first()

if not attendance or not attendance.check_in_time:
    return jsonify({'success': False, 'message': 'Anda belum melakukan check-in hari ini'}), 400
```

#### 2. **Cek Duplikasi Check-out**
```python
if attendance.check_out_time:
    return jsonify({'success': False, 'message': 'Anda sudah melakukan check-out hari ini'}), 400
```

#### 3. **Validasi Lokasi** (sama seperti check-in)

#### 4. **Cek Pulang Cepat**
```python
now = datetime.utcnow()
check_out_time = now.time()
check_out_start = datetime.strptime(Config.CHECK_OUT_START, '%H:%M').time()

# Jika check-out sebelum jam mulai, status = pulang cepat
if attendance.status == 'hadir' and check_out_time < check_out_start:
    attendance.status = 'pulang_cepat'
```

**Konfigurasi:**
- `CHECK_OUT_START`: Jam mulai check-out (default: 16:00)
- `CHECK_OUT_END`: Jam akhir check-out (default: 18:00)

#### 5. **Update Database**
```python
attendance.check_out_time = now
attendance.check_out_latitude = latitude
attendance.check_out_longitude = longitude
attendance.check_out_ip = device_info['ip_address']
attendance.check_out_browser = device_info['browser']
attendance.check_out_os = device_info['os']

db.session.commit()
```

---

## 📍 Validasi Lokasi (Geolocation)

### Formula Haversine

```python
def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Menghitung jarak antara dua koordinat menggunakan formula Haversine
    Returns: jarak dalam meter
    """
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371000  # Radius bumi dalam meter
    
    return c * r
```

### Validasi Radius

```python
def validate_location(latitude, longitude):
    """
    Validasi apakah lokasi berada dalam radius yang diizinkan
    Returns: (is_valid, distance_in_meters)
    """
    distance = calculate_distance(
        Config.OFFICE_LATITUDE,    # Koordinat kantor
        Config.OFFICE_LONGITUDE,
        latitude,                  # Koordinat user
        longitude
    )
    
    is_valid = distance <= Config.GEO_RADIUS_METERS
    return is_valid, distance
```

**Konfigurasi:**
- `OFFICE_LATITUDE`: Latitude kantor (default: -6.2088)
- `OFFICE_LONGITUDE`: Longitude kantor (default: 106.8456)
- `GEO_RADIUS_METERS`: Radius dalam meter (default: 100)

---

## ⏰ Validasi Waktu

### Check-in Time Validation

```python
# Jam mulai check-in: 07:00
# Jam akhir check-in: 09:00

check_in_start = datetime.strptime(Config.CHECK_IN_START, '%H:%M').time()
check_in_end = datetime.strptime(Config.CHECK_IN_END, '%H:%M').time()

# Status berdasarkan waktu
if check_in_time <= check_in_start:
    status = 'hadir'
elif check_in_time <= check_in_end:
    status = 'terlambat'
else:
    # Check-in di luar jam kerja (masih bisa, tapi status terlambat)
    status = 'terlambat'
```

### Check-out Time Validation

```python
# Jam mulai check-out: 16:00
# Jam akhir check-out: 18:00

check_out_start = datetime.strptime(Config.CHECK_OUT_START, '%H:%M').time()

# Cek pulang cepat
if check_out_time < check_out_start:
    attendance.status = 'pulang_cepat'
```

**Catatan:**
- Sistem menggunakan **jam server** (UTC), bukan jam client
- Mencegah manipulasi waktu dari client

---

## 📊 Status Presensi

### Jenis Status

| Status | Deskripsi | Kondisi |
|--------|-----------|---------|
| `hadir` | Hadir tepat waktu | Check-in ≤ jam mulai |
| `terlambat` | Terlambat | Check-in > jam mulai |
| `pulang_cepat` | Pulang sebelum waktunya | Check-out < jam mulai check-out |
| `alpha` | Tidak hadir | Tidak ada check-in |

### Penentuan Status

```python
# Saat Check-in
if check_in_time <= CHECK_IN_START:
    status = 'hadir'
else:
    status = 'terlambat'

# Saat Check-out
if status == 'hadir' and check_out_time < CHECK_OUT_START:
    status = 'pulang_cepat'
```

---

## 📜 Riwayat Presensi

### Filter Berdasarkan Role

#### Karyawan
```python
# Hanya melihat presensi sendiri
query = Attendance.query.filter_by(employee_id=employee_id)
```

#### Atasan
```python
# Melihat presensi bawahan
employee = Employee.query.get(employee_id)
subordinate_ids = [e.id for e in employee.subordinates]
query = Attendance.query.filter(Attendance.employee_id.in_(subordinate_ids))
```

#### HRD/Admin
```python
# Melihat semua presensi
query = Attendance.query
```

### Filter Tanggal

```python
start_date = request.args.get('start_date')
end_date = request.args.get('end_date')

if start_date:
    query = query.filter(Attendance.attendance_date >= start_date)
if end_date:
    query = query.filter(Attendance.attendance_date <= end_date)
```

---

## ⚠️ Error Handling

### 1. Lokasi Tidak Ditemukan
```python
if not latitude or not longitude:
    return jsonify({'success': False, 'message': 'Lokasi tidak ditemukan'}), 400
```

**Penyebab:**
- Browser tidak support Geolocation API
- User menolak permission
- GPS tidak aktif

### 2. Lokasi di Luar Radius
```python
if not is_valid:
    return jsonify({
        'success': False, 
        'message': f'Anda berada di luar radius kantor. Jarak: {distance:.0f}m'
    }), 400
```

**Penyebab:**
- User tidak berada di lokasi kantor
- GPS tidak akurat
- Radius terlalu kecil

### 3. Sudah Check-in Hari Ini
```python
if existing and existing.check_in_time:
    return jsonify({'success': False, 'message': 'Anda sudah melakukan check-in hari ini'}), 400
```

### 4. Belum Check-in
```python
if not attendance or not attendance.check_in_time:
    return jsonify({'success': False, 'message': 'Anda belum melakukan check-in hari ini'}), 400
```

### 5. Data Karyawan Tidak Ditemukan
```python
if not employee_id:
    return jsonify({'success': False, 'message': 'Data karyawan tidak ditemukan'}), 400
```

---

## 📊 Diagram Flow

### Check-in Flow Diagram

```
┌──────────────────┐
│  User Click      │
│  "Check In"      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Request GPS     │
│  Permission      │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  Allowed   Denied
    │         │
    │         └───► Error: Lokasi tidak ditemukan
    │
    ▼
┌──────────────────┐
│  Get Coordinates │
│  (lat, lng)      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Send to Server  │
│  POST /check-in  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Validate        │
│  Employee ID     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Check Duplicate │
│  Check-in        │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  New      Exists
    │         │
    │         └───► Error: Sudah check-in
    │
    ▼
┌──────────────────┐
│  Validate        │
│  Location        │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  Valid     Invalid
    │         │
    │         └───► Error: Di luar radius
    │
    ▼
┌──────────────────┐
│  Get Device Info │
│  (Browser, OS)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Determine       │
│  Status          │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Save to DB      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Log Audit       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Send            │
│  Notification    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Return Success  │
└──────────────────┘
```

---

## 🎯 Contoh Skenario

### Skenario 1: Check-in Berhasil (Tepat Waktu)
1. Karyawan klik "Check In" pukul 07:15
2. Browser minta permission GPS → User izinkan
3. Sistem dapat koordinat: -6.2088, 106.8456
4. Validasi lokasi: ✅ Dalam radius (jarak: 25m)
5. Validasi waktu: Check-in setelah 07:00 → Status: **terlambat**
6. Simpan ke database
7. Notifikasi: "Presensi berhasil"
8. Halaman reload, tombol check-in disabled

### Skenario 2: Check-in Gagal (Lokasi di Luar Radius)
1. Karyawan klik "Check In" dari rumah
2. Sistem dapat koordinat: -6.3000, 106.9000
3. Validasi lokasi: ❌ Di luar radius (jarak: 12.5km)
4. Error: "Anda berada di luar radius kantor. Jarak: 12500m"
5. Check-in gagal, user harus ke kantor

### Skenario 3: Check-out dengan Pulang Cepat
1. Karyawan sudah check-in pukul 07:00 (status: hadir)
2. Karyawan klik "Check Out" pukul 15:30
3. Validasi: ✅ Sudah check-in, ✅ Lokasi valid
4. Cek waktu: Check-out sebelum 16:00 → Status: **pulang_cepat**
5. Update database
6. Notifikasi berhasil

### Skenario 4: Check-out Tanpa Check-in
1. Karyawan langsung klik "Check Out" tanpa check-in
2. Sistem cek: ❌ Tidak ada check-in hari ini
3. Error: "Anda belum melakukan check-in hari ini"
4. Check-out gagal

---

## 📝 Catatan Penting

1. **GPS wajib aktif** untuk presensi
2. **Browser harus support Geolocation API**
3. **User harus izinkan permission** untuk akses lokasi
4. **Lokasi divalidasi menggunakan formula Haversine**
5. **Waktu menggunakan jam server**, bukan jam client
6. **Info perangkat dicatat** untuk audit
7. **Tidak bisa check-in ganda** dalam satu hari
8. **Check-out harus setelah check-in**

---

## 🔧 Konfigurasi

### Location Settings
```python
# config.py
OFFICE_LATITUDE = -6.2088      # Ganti dengan koordinat kantor
OFFICE_LONGITUDE = 106.8456
GEO_RADIUS_METERS = 100        # Radius dalam meter
```

### Time Settings
```python
CHECK_IN_START = '07:00'       # Jam mulai check-in
CHECK_IN_END = '09:00'         # Jam akhir check-in
CHECK_OUT_START = '16:00'      # Jam mulai check-out
CHECK_OUT_END = '18:00'        # Jam akhir check-out
```

---

*Dokumen ini akan diperbarui jika ada perubahan pada flow presensi.*
