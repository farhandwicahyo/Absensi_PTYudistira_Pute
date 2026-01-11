# Flow Autentikasi dan Login

Dokumen ini menjelaskan alur lengkap untuk autentikasi, login, logout, dan manajemen session dalam sistem presensi.

---

## 📋 Daftar Isi

1. [Flow Login](#flow-login)
2. [Flow Logout](#flow-logout)
3. [Session Management](#session-management)
4. [Role-Based Access Control](#role-based-access-control)
5. [Keamanan](#keamanan)
6. [Error Handling](#error-handling)

---

## 🔐 Flow Login

### Alur Lengkap

```
User Mengakses Halaman Login
    ↓
Input Username & Password
    ↓
Validasi Input (tidak kosong)
    ↓
Cari User di Database
    ↓
Verifikasi Password (hash comparison)
    ↓
Cek Status Akun (is_active)
    ↓
Update Last Login & IP Address
    ↓
Deteksi Info Perangkat (Browser, OS, IP)
    ↓
Buat Session (user_id, username, role, employee_id)
    ↓
Log Audit (login_success)
    ↓
Redirect ke Dashboard
```

### Detail Proses

#### 1. **Input Validation**
```python
# Validasi bahwa username dan password tidak kosong
if not username or not password:
    flash('Username dan password harus diisi', 'error')
    return render_template('auth/login.html')
```

#### 2. **User Lookup**
```python
# Cari user berdasarkan username
user = User.query.filter_by(username=username).first()
```

#### 3. **Password Verification**
```python
# Verifikasi password menggunakan Werkzeug security
if user and user.check_password(password):
    # Password cocok
```

**Teknologi:**
- Menggunakan `werkzeug.security.check_password_hash()`
- Password di-hash menggunakan algoritma PBKDF2
- Salt otomatis untuk keamanan

#### 4. **Account Status Check**
```python
if not user.is_active:
    flash('Akun Anda tidak aktif', 'error')
    AuditLogger.log_login(None, username, success=False)
    return render_template('auth/login.html')
```

#### 5. **Update Last Login**
```python
# Deteksi informasi perangkat
device_info = get_device_info()  # Browser, OS, IP

# Update last login
user.last_login = datetime.utcnow()
user.last_login_ip = device_info['ip_address']
db.session.commit()
```

#### 6. **Session Creation**
```python
# Set session variables
session['user_id'] = user.id
session['username'] = user.username
session['role'] = user.role  # admin, hrd, atasan, karyawan
session['employee_id'] = user.employee_id
session.permanent = True  # Session berlaku 8 jam (dari config)
```

#### 7. **Audit Logging**
```python
# Log aktivitas login
AuditLogger.log_login(user.id, user.username, success=True)
```

**Informasi yang dicatat:**
- User ID dan username
- Waktu login
- IP Address
- User Agent (Browser & OS)
- Status (success/failed)

#### 8. **Redirect**
```python
flash('Login berhasil', 'success')
return redirect(url_for('dashboard.index'))
```

---

## 🚪 Flow Logout

### Alur Lengkap

```
User Klik Logout
    ↓
Cek Session (user_id, username)
    ↓
Log Audit (logout)
    ↓
Clear Session (hapus semua data session)
    ↓
Flash Message "Anda telah logout"
    ↓
Redirect ke Halaman Login
```

### Detail Proses

#### 1. **Get Session Info**
```python
user_id = session.get('user_id')
username = session.get('username')
```

#### 2. **Audit Logging**
```python
AuditLogger.log_logout(user_id, username)
```

#### 3. **Clear Session**
```python
session.clear()  # Hapus semua data session
```

#### 4. **Redirect**
```python
flash('Anda telah logout', 'info')
return redirect(url_for('auth.login'))
```

---

## 🔒 Session Management

### Konfigurasi Session

```python
# config.py
PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
```

**Karakteristik:**
- Session berlaku selama **8 jam**
- Session bersifat **permanent** (disimpan di server)
- Session otomatis expire setelah 8 jam tidak aktif

### Session Variables

| Variable | Tipe | Deskripsi |
|----------|------|-----------|
| `user_id` | Integer | ID user di database |
| `username` | String | Username user |
| `role` | String | Role user (admin, hrd, atasan, karyawan) |
| `employee_id` | Integer | ID karyawan (nullable) |

### Session Security

1. **Secret Key**: Digunakan untuk sign session cookie
2. **HTTPOnly**: Cookie tidak bisa diakses JavaScript
3. **Secure**: Cookie hanya dikirim melalui HTTPS (production)
4. **SameSite**: Mencegah CSRF attacks

---

## 🛡️ Role-Based Access Control

### Decorators untuk Proteksi Route

#### 1. `@login_required`
```python
@attendance_bp.route('/')
@login_required
def index():
    # Hanya bisa diakses jika sudah login
    pass
```

**Fungsi:**
- Mengecek apakah `user_id` ada di session
- Jika tidak, redirect ke halaman login
- Jika ada, izinkan akses

#### 2. `@role_required(*roles)`
```python
@employee_bp.route('/')
@role_required('admin', 'hrd')
def index():
    # Hanya bisa diakses oleh admin atau HRD
    pass
```

**Fungsi:**
- Mengecek apakah user sudah login
- Mengecek apakah role user ada dalam list roles yang diizinkan
- Jika tidak, redirect ke dashboard dengan pesan error

#### 3. `@admin_required`
```python
@audit_bp.route('/')
@admin_required
def index():
    # Hanya bisa diakses oleh admin
    pass
```

#### 4. `@hrd_required`
```python
@employee_bp.route('/create')
@hrd_required
def create():
    # Hanya bisa diakses oleh HRD atau admin
    pass
```

#### 5. `@supervisor_required`
```python
@leave_bp.route('/<int:leave_id>/approve')
@supervisor_required
def approve(leave_id):
    # Hanya bisa diakses oleh atasan, HRD, atau admin
    pass
```

---

## 🔐 Keamanan

### 1. Password Hashing

**Algoritma:** PBKDF2 (Password-Based Key Derivation Function 2)

**Implementasi:**
```python
# Saat membuat user
user.set_password('password123')
# Password di-hash dan disimpan sebagai password_hash

# Saat login
user.check_password('password123')
# Membandingkan hash, bukan plain text
```

**Keuntungan:**
- Password tidak pernah disimpan dalam bentuk plain text
- Salt otomatis untuk setiap password
- Resistant terhadap rainbow table attacks

### 2. Session Security

- **Secret Key**: Random string untuk sign session
- **Session Timeout**: 8 jam otomatis expire
- **Session Hijacking Protection**: IP address tracking

### 3. Audit Logging

Semua aktivitas login/logout dicatat:
- Login berhasil/gagal
- Waktu login/logout
- IP address
- User agent (browser & OS)

### 4. Account Status

- Akun bisa dinonaktifkan (`is_active = False`)
- User tidak bisa login jika akun tidak aktif
- Log audit tetap dicatat untuk investigasi

---

## ⚠️ Error Handling

### 1. Username/Password Kosong
```python
if not username or not password:
    flash('Username dan password harus diisi', 'error')
    return render_template('auth/login.html')
```

### 2. Username/Password Salah
```python
if user and user.check_password(password):
    # Login berhasil
else:
    flash('Username atau password salah', 'error')
    AuditLogger.log_login(None, username, success=False)
```

### 3. Akun Tidak Aktif
```python
if not user.is_active:
    flash('Akun Anda tidak aktif', 'error')
    AuditLogger.log_login(None, username, success=False)
    return render_template('auth/login.html')
```

### 4. Lokasi Tidak Ditemukan (untuk presensi)
```python
if not latitude or not longitude:
    return jsonify({'success': False, 'message': 'Lokasi tidak ditemukan'}), 400
```

---

## 📊 Diagram Flow

### Login Flow Diagram

```
┌─────────────────┐
│  User Input     │
│  Username & PWD  │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Validate Input │
│  (not empty)    │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Find User      │
│  in Database    │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Check Password │
│  (hash verify)  │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  Valid    Invalid
    │         │
    │         └───► Flash Error
    │              Log Failed
    │              Return Login Page
    │
    ▼
┌─────────────────┐
│  Check Active   │
│  Status         │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  Active   Inactive
    │         │
    │         └───► Flash Error
    │              Log Failed
    │              Return Login Page
    │
    ▼
┌─────────────────┐
│  Update Last    │
│  Login Info     │
└────────┬─────────┘
         │
    ▼
┌─────────────────┐
│  Create Session │
│  (user_id, role)│
└────────┬─────────┘
         │
    ▼
┌─────────────────┐
│  Log Audit      │
│  (success)      │
└────────┬─────────┘
         │
    ▼
┌─────────────────┐
│  Redirect to    │
│  Dashboard      │
└─────────────────┘
```

---

## 🎯 Contoh Skenario

### Skenario 1: Login Berhasil
1. User mengakses `/auth/login`
2. Input username: `admin` dan password: `admin123`
3. Sistem mencari user dengan username `admin`
4. Password di-verifikasi (hash comparison)
5. Akun aktif, session dibuat
6. Audit log dicatat
7. Redirect ke dashboard

### Skenario 2: Password Salah
1. User input username: `admin` dan password: `wrongpass`
2. Sistem mencari user dengan username `admin`
3. Password tidak cocok
4. Flash error: "Username atau password salah"
5. Audit log dicatat (login_failed)
6. Tetap di halaman login

### Skenario 3: Akun Tidak Aktif
1. User input username: `inactive_user` dan password: `pass123`
2. Sistem mencari user
3. Password cocok
4. Tapi `is_active = False`
5. Flash error: "Akun Anda tidak aktif"
6. Audit log dicatat (login_failed)
7. Tetap di halaman login

### Skenario 4: Session Expire
1. User login dan bekerja selama 8 jam
2. Session otomatis expire
3. User mencoba akses halaman yang protected
4. Decorator `@login_required` mendeteksi tidak ada session
5. Redirect ke halaman login dengan pesan: "Silakan login terlebih dahulu"

---

## 📝 Catatan Penting

1. **Password tidak pernah disimpan dalam plain text**
2. **Session expire otomatis setelah 8 jam**
3. **Semua aktivitas login/logout dicatat di audit log**
4. **IP address dan device info dicatat untuk keamanan**
5. **Akun bisa dinonaktifkan tanpa menghapus data**
6. **Role-based access control di level route dan template**

---

## 🔧 Konfigurasi

### Environment Variables
```bash
SECRET_KEY=your-secret-key-here  # Untuk sign session
```

### Config Settings
```python
# config.py
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
```

---

*Dokumen ini akan diperbarui jika ada perubahan pada flow autentikasi.*
