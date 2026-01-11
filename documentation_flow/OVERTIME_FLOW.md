# Flow Pengajuan Lembur

Dokumen ini menjelaskan alur lengkap untuk pengajuan lembur, approval, dan perhitungan jam lembur dalam sistem presensi.

---

## 📋 Daftar Isi

1. [Flow Pengajuan Lembur](#flow-pengajuan-lembur)
2. [Flow Approval Lembur](#flow-approval-lembur)
3. [Perhitungan Jam Lembur](#perhitungan-jam-lembur)
4. [Alur Approval](#alur-approval)
5. [Notifikasi](#notifikasi)
6. [Error Handling](#error-handling)

---

## 📝 Flow Pengajuan Lembur

### Alur Lengkap

```
Karyawan Klik "Ajukan Lembur"
    ↓
Isi Form (Tanggal, Jam Mulai, Jam Selesai, Alasan)
    ↓
Submit Form (POST /overtime/create)
    ↓
Validasi: Employee ID ada?
    ↓
Cari Data Karyawan (untuk dapat supervisor_id)
    ↓
Hitung Total Jam Lembur
    ↓
Buat Overtime Request
    ↓
Simpan ke Database
    ↓
Log Audit
    ↓
Buat Notifikasi
    ↓
Redirect ke Halaman Lembur
```

### Detail Proses

#### 1. **Form Input**
```html
<form method="POST">
    <input name="overtime_date" type="date" required>
    <input name="start_time" type="time" required>
    <input name="end_time" type="time" required>
    <textarea name="reason" required></textarea>
</form>
```

**Field yang Diperlukan:**
- `overtime_date`: Tanggal lembur
- `start_time`: Jam mulai lembur (format: HH:MM)
- `end_time`: Jam selesai lembur (format: HH:MM)
- `reason`: Alasan lembur

#### 2. **Validasi Employee**
```python
employee_id = session.get('employee_id')
employee = Employee.query.get(employee_id)

if not employee:
    flash('Data karyawan tidak ditemukan', 'error')
    return redirect(url_for('overtime.index'))
```

#### 3. **Perhitungan Total Jam**
```python
start = datetime.strptime(start_time, '%H:%M').time()
end = datetime.strptime(end_time, '%H:%M').time()

start_dt = datetime.combine(datetime.today(), start)
end_dt = datetime.combine(datetime.today(), end)

# Handle jika lembur melewati tengah malam
if end_dt < start_dt:
    end_dt += timedelta(days=1)

total_hours = (end_dt - start_dt).total_seconds() / 3600
```

**Contoh:**
- Start: 18:00, End: 22:00 → Total: 4 jam
- Start: 22:00, End: 02:00 → Total: 4 jam (melewati tengah malam)

#### 4. **Create Overtime Request**
```python
overtime = Overtime(
    employee_id=employee_id,
    overtime_date=datetime.strptime(overtime_date, '%Y-%m-%d').date(),
    start_time=start,
    end_time=end,
    total_hours=total_hours,
    reason=reason,
    supervisor_id=employee.supervisor_id  # Atasan langsung
)
db.session.add(overtime)
db.session.commit()
```

**Status Default:**
- `status`: `menunggu`
- `supervisor_approval`: `False`
- `hrd_approval`: `False`

#### 5. **Audit Logging**
```python
AuditLogger.log_data_change(
    user_id,
    username,
    'create',
    'overtimes',
    overtime.id,
    f'Created overtime request: {total_hours} hours'
)
```

#### 6. **Notifikasi**
```python
NotificationHelper.notify_overtime_submitted(user_id, overtime.id)
```

---

## ✅ Flow Approval Lembur

### Alur Lengkap

```
Atasan/HRD/Admin Melihat Pengajuan
    ↓
Klik Tombol "Approve" atau "Reject"
    ↓
Validasi: Role & Permission
    ↓
Jika Approve:
    - Set Approval Flag
    - Update Status (jika semua approve)
    - Log Audit
    - Notifikasi ke Karyawan
    ↓
Jika Reject:
    - Set Status = ditolak
    - Simpan Alasan Penolakan
    - Log Audit
    - Notifikasi ke Karyawan
```

### Detail Proses Approval

#### 1. **Validasi Role & Permission**

**Atasan:**
```python
if role == 'atasan':
    # Hanya bisa approve pengajuan dari bawahan langsung
    if overtime.supervisor_id != session.get('employee_id'):
        flash('Anda tidak berhak menyetujui pengajuan ini', 'error')
        return redirect(url_for('overtime.index'))
```

**HRD/Admin:**
```python
elif role in ['admin', 'hrd']:
    # Bisa approve semua pengajuan
    pass
```

#### 2. **Proses Approval (Atasan)**
```python
if role == 'atasan':
    overtime.supervisor_approval = True
    overtime.supervisor_approval_date = datetime.utcnow()
    
    # Jika HRD juga perlu approve, tunggu
    if not overtime.hrd_approval:
        # Status tetap menunggu
        pass
    else:
        # Jika HRD sudah approve, status = disetujui
        overtime.status = 'disetujui'
```

#### 3. **Proses Approval (HRD/Admin)**
```python
elif role in ['admin', 'hrd']:
    overtime.hrd_approval = True
    overtime.hrd_approval_date = datetime.utcnow()
    overtime.hrd_id = user_id
    
    # Jika atasan sudah approve, status = disetujui
    if overtime.supervisor_approval:
        overtime.status = 'disetujui'
```

#### 4. **Proses Reject**
```python
overtime.status = 'ditolak'
overtime.rejection_reason = request.form.get('rejection_reason', '')

if role == 'atasan':
    overtime.supervisor_approval = False
elif role in ['admin', 'hrd']:
    overtime.hrd_approval = False
    overtime.hrd_id = user_id
```

---

## 🧮 Perhitungan Jam Lembur

### Formula

```python
def calculate_overtime_hours(start_time, end_time):
    """
    Menghitung total jam lembur
    Handle kasus lembur melewati tengah malam
    """
    start_dt = datetime.combine(datetime.today(), start_time)
    end_dt = datetime.combine(datetime.today(), end_time)
    
    # Jika end < start, berarti melewati tengah malam
    if end_dt < start_dt:
        end_dt += timedelta(days=1)
    
    # Hitung selisih dalam detik, lalu konversi ke jam
    total_seconds = (end_dt - start_dt).total_seconds()
    total_hours = total_seconds / 3600
    
    return total_hours
```

### Contoh Perhitungan

| Start Time | End Time | Total Hours | Keterangan |
|------------|----------|-------------|------------|
| 18:00 | 22:00 | 4.0 | Normal (tidak melewati tengah malam) |
| 22:00 | 02:00 | 4.0 | Melewati tengah malam |
| 17:00 | 20:30 | 3.5 | Setengah jam |
| 19:00 | 19:00 | 24.0 | Satu hari penuh |

---

## 🔄 Alur Approval

### Workflow

```
Karyawan Mengajukan Lembur
    ↓
Status: "menunggu"
Supervisor Approval: False
HRD Approval: False
    ↓
Atasan Review
    ↓
┌─────────┬─────────┐
│ Approve │ Reject  │
└────┬────┴────┬────┘
     │         │
     │         └───► Status: "ditolak"
     │              Supervisor Approval: False
     │
     ▼
Supervisor Approval: True
    ↓
HRD/Admin Review
    ↓
┌─────────┬─────────┐
│ Approve │ Reject  │
└────┬────┴────┬────┘
     │         │
     │         └───► Status: "ditolak"
     │              HRD Approval: False
     │
     ▼
HRD Approval: True
Status: "disetujui"
```

### Status Transitions

| Status | Supervisor Approval | HRD Approval | Deskripsi |
|--------|---------------------|--------------|-----------|
| `menunggu` | False | False | Baru diajukan |
| `menunggu` | True | False | Atasan sudah approve, tunggu HRD |
| `disetujui` | True | True | Semua sudah approve |
| `ditolak` | False/True | False/True | Ditolak oleh salah satu |

---

## 🔔 Notifikasi

### Saat Pengajuan Dibuat
```python
NotificationHelper.notify_overtime_submitted(user_id, overtime_id)
```
**Penerima:** Karyawan yang mengajukan
**Pesan:** "Pengajuan lembur Anda telah dikirim dan menunggu persetujuan."

### Saat Disetujui
```python
NotificationHelper.notify_overtime_approval(user_id, overtime_id, True)
```
**Penerima:** Karyawan yang mengajukan
**Pesan:** "Pengajuan lembur Anda telah disetujui."

### Saat Ditolak
```python
NotificationHelper.notify_overtime_approval(user_id, overtime_id, False)
```
**Penerima:** Karyawan yang mengajukan
**Pesan:** "Pengajuan lembur Anda telah ditolak."

---

## 👥 Siapa Bisa Approve?

### **Atasan**
- ✅ Bisa approve pengajuan dari **bawahan langsung** saja
- ✅ Setelah approve, status tetap `menunggu` (tunggu HRD)
- ✅ Bisa reject dengan alasan

### **HRD**
- ✅ Bisa approve semua pengajuan
- ✅ Bisa approve langsung jika atasan sudah approve
- ✅ Bisa reject dengan alasan

### **Admin**
- ✅ Bisa approve semua pengajuan
- ✅ Bisa approve langsung jika atasan sudah approve
- ✅ Bisa reject dengan alasan

---

## ⚠️ Error Handling

### 1. Data Karyawan Tidak Ditemukan
```python
if not employee:
    flash('Data karyawan tidak ditemukan', 'error')
    return redirect(url_for('overtime.index'))
```

### 2. Tidak Berhak Approve
```python
if overtime.supervisor_id != session.get('employee_id'):
    flash('Anda tidak berhak menyetujui pengajuan ini', 'error')
    return redirect(url_for('overtime.index'))
```

### 3. Form Validation
- Tanggal wajib diisi
- Jam mulai wajib diisi
- Jam selesai wajib diisi
- Alasan wajib diisi

---

## 📊 Diagram Flow

### Pengajuan Lembur Flow

```
┌──────────────────┐
│  Karyawan        │
│  Klik "Ajukan"   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Isi Form        │
│  (Date, Time,    │
│   Reason)        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Submit Form     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Validate        │
│  Employee        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Calculate       │
│  Total Hours     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Create Request  │
│  (Status:        │
│   menunggu)      │
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
│  Redirect        │
└──────────────────┘
```

### Approval Flow

```
┌──────────────────┐
│  Atasan/HRD      │
│  Klik "Approve"  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Validate        │
│  Permission      │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  Valid    Invalid
    │         │
    │         └───► Error: Tidak berhak
    │
    ▼
┌──────────────────┐
│  Set Approval    │
│  Flag            │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Check All       │
│  Approvals       │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  All      Not All
  Approve  Approve
    │         │
    │         └───► Status: menunggu
    │
    ▼
┌──────────────────┐
│  Status:         │
│  disetujui       │
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
└──────────────────┘
```

---

## 🎯 Contoh Skenario

### Skenario 1: Pengajuan Lembur Normal
1. **Karyawan A** mengajukan lembur:
   - Tanggal: 2024-01-15
   - Jam: 18:00 - 22:00
   - Alasan: Menyelesaikan project
2. Sistem hitung: 4 jam
3. Status: `menunggu`
4. Notifikasi ke karyawan: "Pengajuan dikirim"
5. **Atasan B** melihat dan approve
6. Status: `menunggu` (tunggu HRD)
7. **HRD C** melihat dan approve
8. Status: `disetujui`
9. Notifikasi ke karyawan: "Pengajuan disetujui"

### Skenario 2: Lembur Melewati Tengah Malam
1. **Karyawan A** mengajukan lembur:
   - Tanggal: 2024-01-15
   - Jam: 22:00 - 02:00
   - Alasan: Shift malam
2. Sistem hitung: 4 jam (handle melewati tengah malam)
3. Status: `menunggu`
4. Approval flow sama seperti skenario 1

### Skenario 3: Pengajuan Ditolak
1. **Karyawan A** mengajukan lembur
2. **Atasan B** melihat dan reject dengan alasan: "Tidak urgent"
3. Status: `ditolak`
4. Notifikasi ke karyawan: "Pengajuan ditolak"

---

## 📝 Catatan Penting

1. **Total jam dihitung otomatis** dari jam mulai dan selesai
2. **Sistem handle lembur melewati tengah malam**
3. **Approval 2 tahap**: Atasan → HRD/Admin
4. **Atasan hanya bisa approve bawahan langsung**
5. **Semua aktivitas dicatat di audit log**
6. **Notifikasi otomatis dikirim** ke semua pihak

---

*Dokumen ini akan diperbarui jika ada perubahan pada flow lembur.*
