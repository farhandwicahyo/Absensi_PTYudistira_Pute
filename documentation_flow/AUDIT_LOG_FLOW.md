# Flow Audit Log

Dokumen ini menjelaskan alur lengkap untuk audit logging dalam sistem presensi, termasuk pencatatan aktivitas, penyimpanan, dan pengaksesan log.

---

## 📋 Daftar Isi

1. [Overview Audit Log](#overview-audit-log)
2. [Flow Pencatatan Log](#flow-pencatatan-log)
3. [Jenis Aktivitas yang Dicatat](#jenis-aktivitas-yang-dicatat)
4. [Flow Melihat Audit Log](#flow-melihat-audit-log)
5. [Filter dan Pencarian](#filter-dan-pencarian)
6. [Keamanan Log](#keamanan-log)

---

## 📝 Overview Audit Log

### Tujuan
- **Transparansi**: Mencatat semua aktivitas penting
- **Keamanan**: Deteksi aktivitas mencurigakan
- **Compliance**: Memenuhi kebutuhan audit internal/eksternal
- **Investigasi**: Melacak masalah atau insiden

### Karakteristik
- **Immutable**: Log tidak bisa diubah atau dihapus
- **Comprehensive**: Mencatat semua aktivitas penting
- **Detailed**: Menyimpan informasi lengkap (user, waktu, IP, dll)
- **Searchable**: Bisa difilter dan dicari

---

## 🔄 Flow Pencatatan Log

### Alur Lengkap

```
Aktivitas Terjadi (Login, Presensi, dll)
    ↓
Panggil AuditLogger
    ↓
Buat AuditLog Object
    ↓
Set: User ID, Username, Activity, Action, dll
    ↓
Deteksi Info Perangkat (IP, User Agent)
    ↓
Simpan ke Database
    ↓
Commit Transaction
```

### Detail Proses

#### 1. **Generic Log Method**
```python
@staticmethod
def log(user_id, username, activity, action, table_name=None, record_id=None, details=None):
    log = AuditLog(
        user_id=user_id,
        username=username,
        activity=activity,        # login, presensi, data_change, dll
        action=action,            # create, update, delete, login_success, dll
        table_name=table_name,   # employees, attendances, dll
        record_id=record_id,      # ID record yang terpengaruh
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        details=details          # JSON atau text detail tambahan
    )
    db.session.add(log)
    db.session.commit()
```

#### 2. **Specific Log Methods**
```python
# Login
AuditLogger.log_login(user_id, username, success=True)

# Logout
AuditLogger.log_logout(user_id, username)

# Presensi
AuditLogger.log_presensi(user_id, username, action, attendance_id, details)

# Data Change
AuditLogger.log_data_change(user_id, username, action, table_name, record_id, details)
```

---

## 📊 Jenis Aktivitas yang Dicatat

### 1. **Login/Logout**

#### Login Berhasil
```python
AuditLogger.log_login(user_id, username, success=True)
```
**Data yang Dicatat:**
- User ID dan username
- Activity: `login`
- Action: `login_success`
- IP address
- User agent
- Timestamp

#### Login Gagal
```python
AuditLogger.log_login(None, username, success=False)
```
**Data yang Dicatat:**
- Username (user_id = None karena gagal)
- Activity: `login`
- Action: `login_failed`
- IP address
- User agent
- Timestamp

#### Logout
```python
AuditLogger.log_logout(user_id, username)
```
**Data yang Dicatat:**
- User ID dan username
- Activity: `logout`
- Action: `logout`
- IP address
- User agent
- Timestamp

---

### 2. **Presensi**

#### Check-in
```python
AuditLogger.log_presensi(
    user_id,
    username,
    'check_in',
    attendance_id,
    f'Location: {latitude}, {longitude}'
)
```
**Data yang Dicatat:**
- User ID dan username
- Activity: `presensi`
- Action: `check_in`
- Table: `attendances`
- Record ID: `attendance_id`
- Details: Koordinat GPS
- IP address
- User agent
- Timestamp

#### Check-out
```python
AuditLogger.log_presensi(
    user_id,
    username,
    'check_out',
    attendance_id,
    f'Location: {latitude}, {longitude}'
)
```

---

### 3. **Perubahan Data**

#### Create
```python
AuditLogger.log_data_change(
    user_id,
    username,
    'create',
    'employees',
    employee_id,
    f'Created employee: {full_name}'
)
```

#### Update
```python
AuditLogger.log_data_change(
    user_id,
    username,
    'update',
    'employees',
    employee_id,
    f'Updated employee: {full_name}'
)
```

#### Delete
```python
AuditLogger.log_data_change(
    user_id,
    username,
    'delete',
    'employees',
    employee_id,
    f'Deleted employee: {full_name}'
)
```

---

### 4. **Approval**

#### Approve Leave Request
```python
AuditLogger.log_data_change(
    user_id,
    username,
    'approve',
    'leave_requests',
    leave_request_id,
    f'Approved {leave_type} request'
)
```

#### Reject Leave Request
```python
AuditLogger.log_data_change(
    user_id,
    username,
    'reject',
    'leave_requests',
    leave_request_id,
    f'Rejected {leave_type} request'
)
```

---

## 👁️ Flow Melihat Audit Log

### Alur Lengkap

```
Admin Klik "Audit Log"
    ↓
Load Halaman (GET /audit/)
    ↓
Get Filter Parameters (Date, Activity)
    ↓
Query AuditLog dengan Filter
    ↓
Order by Created At (Desc)
    ↓
Limit 1000 Records
    ↓
Render Table
```

### Detail Proses

#### 1. **Query dengan Filter**
```python
query = AuditLog.query

# Date filter
if start_date:
    query = query.filter(AuditLog.created_at >= start_date)
if end_date:
    query = query.filter(AuditLog.created_at <= end_date)

# Activity filter
if activity:
    query = query.filter(AuditLog.activity == activity)

logs = query.order_by(AuditLog.created_at.desc()).limit(1000).all()
```

#### 2. **Render Table**
```html
<table>
    <thead>
        <tr>
            <th>Waktu</th>
            <th>User</th>
            <th>Aktivitas</th>
            <th>Aksi</th>
            <th>Tabel</th>
            <th>IP Address</th>
        </tr>
    </thead>
    <tbody>
        {% for log in logs %}
        <tr>
            <td>{{ log.created_at.strftime('%d/%m/%Y %H:%M:%S') }}</td>
            <td>{{ log.username or '-' }}</td>
            <td>{{ log.activity }}</td>
            <td>{{ log.action }}</td>
            <td>{{ log.table_name or '-' }}</td>
            <td>{{ log.ip_address or '-' }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

---

## 🔍 Filter dan Pencarian

### Filter yang Tersedia

#### 1. **Filter Tanggal**
```html
<input type="date" name="start_date" value="{{ request.args.get('start_date', '') }}">
<input type="date" name="end_date" value="{{ request.args.get('end_date', '') }}">
```

**Fungsi:**
- Filter log berdasarkan rentang tanggal
- Default: Semua tanggal

#### 2. **Filter Aktivitas**
```html
<select name="activity">
    <option value="">Semua</option>
    <option value="login">Login</option>
    <option value="logout">Logout</option>
    <option value="presensi">Presensi</option>
    <option value="data_change">Perubahan Data</option>
</select>
```

**Fungsi:**
- Filter log berdasarkan jenis aktivitas
- Default: Semua aktivitas

---

## 🔒 Keamanan Log

### 1. **Immutable Log**
- Log **tidak bisa diubah** setelah dibuat
- Log **tidak bisa dihapus** (untuk compliance)
- Hanya bisa **ditambah** log baru

### 2. **Access Control**
- Hanya **Admin** yang bisa melihat audit log
- Decorator: `@admin_required`
- User lain tidak bisa akses

### 3. **Data Privacy**
- Log menyimpan informasi sensitif (IP, user agent)
- Hanya admin yang berwenang bisa akses
- Log tidak boleh dibagikan ke pihak luar tanpa izin

### 4. **Error Handling**
```python
try:
    log = AuditLog(...)
    db.session.add(log)
    db.session.commit()
except Exception as e:
    db.session.rollback()
    print(f"Error logging audit: {str(e)}")
    # Jangan crash aplikasi jika log gagal
```

---

## 📊 Diagram Flow

### Audit Log Flow

```
┌──────────────────┐
│  Activity        │
│  Occurs          │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Call            │
│  AuditLogger     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Get Request     │
│  Info (IP, UA)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Create          │
│  AuditLog        │
│  Object          │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Save to DB      │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  Success   Error
    │         │
    │         └───► Rollback, Log Error
    │              (Don't crash app)
    │
    ▼
┌──────────────────┐
│  Log Saved       │
└──────────────────┘
```

### View Audit Log Flow

```
┌──────────────────┐
│  Admin Klik      │
│  "Audit Log"     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Check Role      │
│  (Admin only)    │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  Admin    Not Admin
    │         │
    │         └───► Error: Unauthorized
    │
    ▼
┌──────────────────┐
│  Get Filter      │
│  Parameters      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Query Logs      │
│  with Filters    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Order & Limit   │
│  (1000 records)  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Render Table    │
└──────────────────┘
```

---

## 🎯 Contoh Skenario

### Skenario 1: Login Berhasil
1. User login dengan username: `admin`
2. Sistem buat log:
   - User: admin
   - Activity: login
   - Action: login_success
   - IP: 192.168.1.1
   - Time: 2024-01-15 08:00:00
3. Log tersimpan di database

### Skenario 2: Presensi Check-in
1. Karyawan check-in
2. Sistem buat log:
   - User: karyawan1
   - Activity: presensi
   - Action: check_in
   - Table: attendances
   - Record ID: 123
   - Details: Location: -6.2088, 106.8456
   - IP: 192.168.1.2
   - Time: 2024-01-15 07:15:00

### Skenario 3: Edit Karyawan
1. HRD edit data karyawan
2. Sistem buat log:
   - User: hrd1
   - Activity: data_change
   - Action: update
   - Table: employees
   - Record ID: 5
   - Details: Updated employee: John Doe
   - IP: 192.168.1.3
   - Time: 2024-01-15 10:30:00

### Skenario 4: View Audit Log dengan Filter
1. Admin buka halaman Audit Log
2. Set filter:
   - Start Date: 2024-01-01
   - End Date: 2024-01-31
   - Activity: login
3. Sistem query: Log login di bulan Januari 2024
4. Tampilkan hasil di table

---

## 📝 Catatan Penting

1. **Log tidak bisa diubah atau dihapus** (immutable)
2. **Hanya Admin** yang bisa melihat audit log
3. **Error handling**: Log failure tidak crash aplikasi
4. **Comprehensive**: Semua aktivitas penting dicatat
5. **Detailed**: Menyimpan informasi lengkap
6. **Searchable**: Bisa difilter berdasarkan tanggal dan aktivitas
7. **Limit**: Maksimal 1000 records ditampilkan (untuk performa)

---

## 🔧 Konfigurasi

### Database Schema
```python
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    username = db.Column(db.String(50), nullable=True)
    activity = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    table_name = db.Column(db.String(50), nullable=True)
    record_id = db.Column(db.Integer, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

*Dokumen ini akan diperbarui jika ada perubahan pada flow audit log.*
