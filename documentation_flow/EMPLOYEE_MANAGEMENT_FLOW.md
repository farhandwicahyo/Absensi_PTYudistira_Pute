# Flow Manajemen Data Karyawan

Dokumen ini menjelaskan alur lengkap untuk manajemen data karyawan termasuk CRUD (Create, Read, Update, Delete), Import/Export, dan validasi data.

---

## 📋 Daftar Isi

1. [Flow Tambah Karyawan](#flow-tambah-karyawan)
2. [Flow Edit Karyawan](#flow-edit-karyawan)
3. [Flow Hapus/Nonaktifkan Karyawan](#flow-hapusnonaktifkan-karyawan)
4. [Flow Import Data](#flow-import-data)
5. [Flow Export Data](#flow-export-data)
6. [Validasi Data](#validasi-data)
7. [Hak Akses](#hak-akses)

---

## ➕ Flow Tambah Karyawan

### Alur Lengkap

```
HRD/Admin Klik "Tambah Karyawan"
    ↓
Isi Form (NIK, Nama, Email, dll)
    ↓
Submit Form (POST /employee/create)
    ↓
Validasi: NIK unik?
    ↓
Validasi: Email unik?
    ↓
Buat Employee Record
    ↓
Simpan ke Database
    ↓
Log Audit
    ↓
Redirect ke Daftar Karyawan
```

### Detail Proses

#### 1. **Form Input**
```html
<form method="POST">
    <input name="nik" required>           <!-- NIK (unique) -->
    <input name="full_name" required>    <!-- Nama lengkap -->
    <input name="email" type="email" required>  <!-- Email (unique) -->
    <input name="phone">                  <!-- Nomor HP (optional) -->
    <input name="position" required>      <!-- Jabatan -->
    <input name="division" required>      <!-- Divisi -->
    <select name="supervisor_id">        <!-- Atasan langsung (optional) -->
    <input name="hire_date" type="date"> <!-- Tanggal masuk (optional) -->
</form>
```

#### 2. **Validasi NIK Unik**
```python
if Employee.query.filter_by(nik=nik).first():
    flash('NIK sudah terdaftar', 'error')
    return render_template('employee/create.html')
```

#### 3. **Validasi Email Unik**
```python
if Employee.query.filter_by(email=email).first():
    flash('Email sudah terdaftar', 'error')
    return render_template('employee/create.html')
```

#### 4. **Create Employee**
```python
employee = Employee(
    nik=nik,
    full_name=full_name,
    email=email,
    phone=phone,
    position=position,
    division=division,
    supervisor_id=int(supervisor_id) if supervisor_id else None,
    hire_date=datetime.strptime(hire_date, '%Y-%m-%d').date() if hire_date else None,
    status='aktif'  # Default status
)
db.session.add(employee)
db.session.commit()
```

#### 5. **Audit Logging**
```python
AuditLogger.log_data_change(
    user_id,
    username,
    'create',
    'employees',
    employee.id,
    f'Created employee: {full_name}'
)
```

---

## ✏️ Flow Edit Karyawan

### Alur Lengkap

```
HRD/Admin Klik "Edit" pada Karyawan
    ↓
Load Data Karyawan dari Database
    ↓
Tampilkan Form dengan Data Existing
    ↓
User Edit Data
    ↓
Submit Form (POST /employee/<id>/edit)
    ↓
Validasi: NIK unik? (kecuali untuk karyawan yang sama)
    ↓
Validasi: Email unik? (kecuali untuk karyawan yang sama)
    ↓
Update Employee Record
    ↓
Simpan ke Database
    ↓
Log Audit
    ↓
Redirect ke Daftar Karyawan
```

### Detail Proses

#### 1. **Load Existing Data**
```python
employee = Employee.query.get_or_404(employee_id)
```

#### 2. **Update Data**
```python
employee.nik = request.form.get('nik')
employee.full_name = request.form.get('full_name')
employee.email = request.form.get('email')
employee.phone = request.form.get('phone')
employee.position = request.form.get('position')
employee.division = request.form.get('division')
employee.supervisor_id = int(request.form.get('supervisor_id')) if request.form.get('supervisor_id') else None
employee.status = request.form.get('status')

if request.form.get('hire_date'):
    employee.hire_date = datetime.strptime(request.form.get('hire_date'), '%Y-%m-%d').date()

db.session.commit()
```

#### 3. **Audit Logging**
```python
AuditLogger.log_data_change(
    user_id,
    username,
    'update',
    'employees',
    employee.id,
    f'Updated employee: {employee.full_name}'
)
```

---

## 🗑️ Flow Hapus/Nonaktifkan Karyawan

### Alur Lengkap

```
HRD/Admin Klik "Hapus" pada Karyawan
    ↓
Konfirmasi: "Yakin ingin menonaktifkan?"
    ↓
Submit (POST /employee/<id>/delete)
    ↓
Soft Delete: Ubah Status = 'nonaktif'
    ↓
Simpan ke Database
    ↓
Log Audit
    ↓
Redirect ke Daftar Karyawan
```

### Detail Proses

**Catatan:** Sistem menggunakan **soft delete**, bukan hard delete. Data tetap ada di database, hanya status yang diubah.

```python
employee = Employee.query.get_or_404(employee_id)

# Soft delete (ubah status)
employee.status = 'nonaktif'
db.session.commit()

# Log audit
AuditLogger.log_data_change(
    user_id,
    username,
    'delete',
    'employees',
    employee.id,
    f'Deleted employee: {employee.full_name}'
)
```

**Keuntungan Soft Delete:**
- Data tidak hilang (untuk audit)
- Bisa diaktifkan kembali
- Riwayat tetap terjaga

---

## 📥 Flow Import Data

### Alur Lengkap

```
HRD/Admin Klik "Import"
    ↓
Pilih File CSV
    ↓
Upload File (POST /employee/import)
    ↓
Baca File CSV
    ↓
Loop Setiap Baris:
    - Validasi NIK unik
    - Validasi Email unik
    - Buat Employee Record
    ↓
Simpan ke Database
    ↓
Tampilkan Hasil (Berhasil X, Error Y)
    ↓
Redirect ke Daftar Karyawan
```

### Detail Proses

#### 1. **Format CSV**
```csv
nik,full_name,email,phone,position,division,status
EMP001,John Doe,john@company.com,081234567890,Developer,IT,aktif
EMP002,Jane Smith,jane@company.com,081234567891,Designer,Design,aktif
```

#### 2. **Baca File**
```python
stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
csv_input = csv.DictReader(stream)
```

#### 3. **Process Each Row**
```python
imported = 0
errors = []

for row in csv_input:
    try:
        # Check if exists
        if Employee.query.filter_by(nik=row['nik']).first():
            errors.append(f"NIK {row['nik']} sudah terdaftar")
            continue
        
        # Create employee
        employee = Employee(
            nik=row['nik'],
            full_name=row['full_name'],
            email=row['email'],
            phone=row.get('phone'),
            position=row['position'],
            division=row['division'],
            status=row.get('status', 'aktif')
        )
        db.session.add(employee)
        imported += 1
    except Exception as e:
        errors.append(f"Error importing {row.get('nik', 'unknown')}: {str(e)}")

db.session.commit()
```

#### 4. **Tampilkan Hasil**
```python
flash(f'Berhasil mengimport {imported} data karyawan', 'success')
if errors:
    flash(f'Terjadi {len(errors)} error: {", ".join(errors[:5])}', 'warning')
```

---

## 📤 Flow Export Data

### Alur Lengkap

```
HRD/Admin Klik "Export"
    ↓
Query Semua Employee dari Database
    ↓
Generate CSV File
    ↓
Download File CSV
```

### Detail Proses

#### 1. **Query Data**
```python
employees = Employee.query.all()
```

#### 2. **Generate CSV**
```python
output = io.StringIO()
writer = csv.writer(output)

# Header
writer.writerow(['NIK', 'Nama Lengkap', 'Email', 'Phone', 'Jabatan', 'Divisi', 'Status'])

# Data
for emp in employees:
    writer.writerow([
        emp.nik,
        emp.full_name,
        emp.email,
        emp.phone or '',
        emp.position,
        emp.division,
        emp.status
    ])

output.seek(0)
```

#### 3. **Download File**
```python
return send_file(
    io.BytesIO(output.getvalue().encode()),
    mimetype='text/csv',
    as_attachment=True,
    download_name=f'employees_{datetime.now().strftime("%Y%m%d")}.csv'
)
```

---

## ✅ Validasi Data

### 1. **NIK (Nomor Induk Karyawan)**
- ✅ Wajib diisi
- ✅ Harus unik (tidak boleh duplikat)
- ✅ Format: String (bisa alphanumeric)

### 2. **Nama Lengkap**
- ✅ Wajib diisi
- ✅ Format: String

### 3. **Email**
- ✅ Wajib diisi
- ✅ Harus unik (tidak boleh duplikat)
- ✅ Format: Valid email format

### 4. **Nomor HP**
- ⚠️ Optional (boleh kosong)
- Format: String

### 5. **Jabatan**
- ✅ Wajib diisi
- Format: String

### 6. **Divisi**
- ✅ Wajib diisi
- Format: String

### 7. **Atasan Langsung**
- ⚠️ Optional (boleh kosong)
- Harus referensi ke Employee yang valid

### 8. **Tanggal Masuk**
- ⚠️ Optional (boleh kosong)
- Format: Date (YYYY-MM-DD)

### 9. **Status**
- Default: `aktif`
- Pilihan: `aktif`, `nonaktif`

---

## 🔒 Hak Akses

### Role yang Bisa Akses

| Fitur | Karyawan | Atasan | HRD | Admin |
|-------|----------|--------|-----|-------|
| Lihat Daftar | ❌ | ❌ | ✅ | ✅ |
| Tambah | ❌ | ❌ | ✅ | ✅ |
| Edit | ❌ | ❌ | ✅ | ✅ |
| Hapus | ❌ | ❌ | ✅ | ✅ |
| Import | ❌ | ❌ | ✅ | ✅ |
| Export | ❌ | ❌ | ✅ | ✅ |

**Decorator:** `@hrd_required` (hanya HRD dan Admin)

---

## 📊 Diagram Flow

### Tambah Karyawan Flow

```
┌──────────────────┐
│  HRD/Admin       │
│  Klik "Tambah"   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Isi Form        │
│  (NIK, Nama,     │
│   Email, dll)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Submit Form     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Validate NIK    │
│  (unique?)       │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  Unique   Duplicate
    │         │
    │         └───► Error: NIK sudah terdaftar
    │
    ▼
┌──────────────────┐
│  Validate Email  │
│  (unique?)       │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  Unique   Duplicate
    │         │
    │         └───► Error: Email sudah terdaftar
    │
    ▼
┌──────────────────┐
│  Create Employee │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Save to DB       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Log Audit       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Redirect        │
└──────────────────┘
```

---

## 🎯 Contoh Skenario

### Skenario 1: Tambah Karyawan Berhasil
1. HRD klik "Tambah Karyawan"
2. Isi form:
   - NIK: EMP001
   - Nama: John Doe
   - Email: john@company.com
   - Jabatan: Developer
   - Divisi: IT
3. Submit form
4. Validasi: ✅ NIK unik, ✅ Email unik
5. Employee record dibuat
6. Audit log dicatat
7. Redirect ke daftar karyawan

### Skenario 2: NIK Duplikat
1. HRD coba tambah karyawan dengan NIK: EMP001
2. Sistem cek: NIK sudah ada
3. Error: "NIK sudah terdaftar"
4. Tetap di form, user bisa edit NIK

### Skenario 3: Import CSV
1. HRD klik "Import"
2. Pilih file CSV dengan 10 data karyawan
3. Upload file
4. Sistem proses:
   - 8 data berhasil (NIK unik)
   - 2 data error (NIK duplikat)
5. Flash: "Berhasil mengimport 8 data karyawan"
6. Flash: "Terjadi 2 error: NIK EMP001 sudah terdaftar, NIK EMP002 sudah terdaftar"

### Skenario 4: Nonaktifkan Karyawan
1. HRD klik "Hapus" pada karyawan
2. Konfirmasi: "Yakin ingin menonaktifkan karyawan ini?"
3. User klik "OK"
4. Status karyawan diubah menjadi `nonaktif`
5. Audit log dicatat
6. Karyawan tidak muncul di daftar aktif (bisa difilter)

---

## 📝 Catatan Penting

1. **Soft Delete**: Karyawan tidak dihapus, hanya dinonaktifkan
2. **NIK dan Email harus unik**: Tidak boleh duplikat
3. **Import CSV**: Format harus sesuai, error handling untuk setiap baris
4. **Export CSV**: Semua data karyawan diekspor
5. **Audit Log**: Semua perubahan dicatat
6. **Hanya HRD/Admin**: Yang bisa akses fitur ini

---

*Dokumen ini akan diperbarui jika ada perubahan pada flow manajemen karyawan.*
