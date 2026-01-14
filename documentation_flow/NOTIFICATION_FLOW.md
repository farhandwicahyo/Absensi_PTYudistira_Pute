# Flow Notifikasi Sistem

Dokumen ini menjelaskan alur lengkap untuk sistem notifikasi dalam aplikasi presensi, termasuk pembuatan, pengiriman, dan manajemen notifikasi.

---

## 📋 Daftar Isi

1. [Overview Notifikasi](#overview-notifikasi)
2. [Jenis Notifikasi](#jenis-notifikasi)
3. [Flow Pembuatan Notifikasi](#flow-pembuatan-notifikasi)
4. [Flow Menampilkan Notifikasi](#flow-menampilkan-notifikasi)
5. [Flow Mark as Read](#flow-mark-as-read)
6. [Notifikasi per Event](#notifikasi-per-event)

---

## 📢 Overview Notifikasi

### Tujuan

- Memberikan informasi real-time kepada user
- Meningkatkan engagement dan awareness
- Memastikan user tidak melewatkan informasi penting

### Karakteristik

- **Real-time**: Notifikasi dibuat saat event terjadi
- **Role-based**: Notifikasi dikirim ke user yang relevan
- **Persistent**: Notifikasi tersimpan di database
- **Read/Unread**: Status bisa ditandai sudah dibaca

---

## 📨 Jenis Notifikasi

### 1. **Presensi**

- `presensi`: Notifikasi terkait presensi
  - Presensi berhasil
  - Presensi gagal

### 2. **Leave (Timeoff)**

- `leave`: Notifikasi terkait pengajuan Timeoff
  - Pengajuan dikirim
  - Pengajuan disetujui
  - Pengajuan ditolak
  - Pengajuan baru (untuk atasan)
  - Menunggu approval HRD (untuk HRD)

### 3. **Overtime (Lembur)**

- `overtime`: Notifikasi terkait pengajuan lembur
  - Pengajuan dikirim
  - Pengajuan disetujui
  - Pengajuan ditolak

### 4. **System**

- `system`: Notifikasi sistem umum
  - Update sistem
  - Maintenance
  - Pengumuman

---

## 🔄 Flow Pembuatan Notifikasi

### Alur Lengkap

```
Event Terjadi (Presensi, Approval, dll)
    ↓
Panggil NotificationHelper
    ↓
Buat Notification Object
    ↓
Set User ID, Title, Message, Type
    ↓
Simpan ke Database
    ↓
Return Notification Object
```

### Detail Proses

#### 1. **Create Notification (Generic)**

```python
def create_notification(user_id, title, message, notification_type, related_id=None):
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
        related_id=related_id,  # ID terkait (attendance_id, leave_request_id, dll)
        is_read=False
    )
    db.session.add(notification)
    db.session.commit()
    return notification
```

#### 2. **Helper Methods**

```python
# Presensi berhasil
notify_presensi_success(user_id, attendance_id)

# Presensi gagal
notify_presensi_failed(user_id, reason)

# Pengajuan izin/cuti dikirim
notify_leave_submitted(user_id, leave_request_id, leave_type)

# Approval izin/cuti
notify_leave_approval(user_id, leave_request_id, approved, leave_type)

# Pengajuan lembur dikirim
notify_overtime_submitted(user_id, overtime_id)

# Approval lembur
notify_overtime_approval(user_id, overtime_id, approved)
```

---

## 👁️ Flow Menampilkan Notifikasi

### Alur Lengkap

```
User Login / Load Dashboard
    ↓
JavaScript: Fetch Notifications (GET /notification/unread)
    ↓
Backend: Query Notifications (is_read = False)
    ↓
Return JSON Array
    ↓
Frontend: Render Notifications
    ↓
Tampilkan Badge Count
    ↓
Tampilkan Dropdown List
```

### Detail Proses

#### 1. **Backend API**

```python
@notification_bp.route('/unread')
@login_required
def unread():
    user_id = session.get('user_id')
    notifications = Notification.query.filter_by(
        user_id=user_id,
        is_read=False
    ).order_by(Notification.created_at.desc()).all()

    return jsonify([n.to_dict() for n in notifications])
```

#### 2. **Frontend Fetch**

```javascript
function loadNotifications() {
  fetch("/notification/unread")
    .then((response) => response.json())
    .then((data) => {
      const badge = document.getElementById("notificationBadge");
      const list = document.getElementById("notificationList");

      if (data.length > 0) {
        badge.textContent = data.length;
        badge.classList.remove("hidden");

        // Render notifications
        list.innerHTML = data
          .map(
            (n) => `
                    <div class="notification-item">
                        <h4>${n.title}</h4>
                        <p>${n.message}</p>
                        <span>${new Date(n.created_at).toLocaleString(
                          "id-ID"
                        )}</span>
                    </div>
                `
          )
          .join("");
      } else {
        badge.classList.add("hidden");
        list.innerHTML = "<div>Tidak ada notifikasi</div>";
      }
    });
}
```

#### 3. **Auto Load**

```javascript
// Load saat dropdown dibuka
document
  .getElementById("notificationBtn")
  .addEventListener("click", function () {
    loadNotifications();
  });

// Auto load setiap 30 detik (optional)
setInterval(loadNotifications, 30000);
```

---

## ✅ Flow Mark as Read

### Alur Lengkap

```
User Klik Notifikasi
    ↓
JavaScript: POST /notification/<id>/read
    ↓
Backend: Update is_read = True
    ↓
Return Success
    ↓
Frontend: Reload Notifications
```

### Detail Proses

#### 1. **Mark Single as Read**

```python
@notification_bp.route('/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_read(notification_id):
    user_id = session.get('user_id')
    notification = Notification.query.get_or_404(notification_id)

    # Security: hanya bisa mark read notifikasi sendiri
    if notification.user_id != user_id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    notification.is_read = True
    db.session.commit()

    return jsonify({'success': True})
```

#### 2. **Mark All as Read**

```python
@notification_bp.route('/read-all', methods=['POST'])
@login_required
def mark_all_read():
    user_id = session.get('user_id')
    Notification.query.filter_by(
        user_id=user_id,
        is_read=False
    ).update({'is_read': True})
    db.session.commit()

    return jsonify({'success': True})
```

#### 3. **Frontend**

```javascript
function markRead(id) {
  fetch(`/notification/${id}/read`, { method: "POST" }).then(() =>
    loadNotifications()
  );
}
```

---

## 🎯 Notifikasi per Event

### 1. **Presensi Berhasil**

**Trigger:** Setelah check-in/check-out berhasil

```python
NotificationHelper.notify_presensi_success(user_id, attendance_id)
```

**Penerima:** Karyawan yang melakukan presensi

**Pesan:**

- Title: "Presensi Berhasil"
- Message: "Presensi Anda telah berhasil dicatat."

---

### 2. **Presensi Gagal**

**Trigger:** Presensi gagal (lokasi di luar radius, dll)

```python
NotificationHelper.notify_presensi_failed(user_id, reason)
```

**Penerima:** Karyawan yang mencoba presensi

**Pesan:**

- Title: "Presensi Gagal"
- Message: "Presensi gagal: {reason}"

---

### 3. **Pengajuan Timeoff Dikirim**

**Trigger:** Karyawan mengajukan Timeoff

```python
NotificationHelper.notify_leave_submitted(user_id, leave_request_id, leave_type)
```

**Penerima:** Karyawan yang mengajukan

**Pesan:**

- Title: "Pengajuan {leave_type} Dikirim"
- Message: "Pengajuan {leave_type} Anda telah dikirim dan menunggu persetujuan."

---

### 4. **Pengajuan Baru untuk Atasan**

**Trigger:** Karyawan mengajukan Timeoff (jika ada atasan)

```python
NotificationHelper.notify_supervisor_new_leave(
    supervisor_user_id,
    leave_request_id,
    leave_type,
    employee_name
)
```

**Penerima:** Atasan langsung

**Pesan:**

- Title: "Pengajuan {leave_type} Baru"
- Message: "{employee_name} mengajukan {leave_type}. Silakan review dan approve."

---

### 5. **Pengajuan Disetujui/Ditolak**

**Trigger:** Atasan/HRD approve atau reject pengajuan

```python
NotificationHelper.notify_leave_approval(
    user_id,
    leave_request_id,
    approved,  # True/False
    leave_type
)
```

**Penerima:** Karyawan yang mengajukan

**Pesan:**

- Title: "Pengajuan {leave_type} {status}"
- Message: "Pengajuan {leave_type} Anda telah {status}."

---

### 6. **Cuti Menunggu Approval HRD**

**Trigger:** Atasan approve cuti (cuti perlu approval HRD juga)

```python
NotificationHelper.notify_hrd_pending_leave(
    hrd_user_id,
    leave_request_id,
    employee_name
)
```

**Penerima:** Semua user dengan role HRD/Admin

**Pesan:**

- Title: "Pengajuan Cuti Menunggu Approval HRD"
- Message: "Pengajuan cuti dari {employee_name} telah disetujui atasan dan menunggu approval HRD."

---

### 7. **Pengajuan Lembur Dikirim**

**Trigger:** Karyawan mengajukan lembur

```python
NotificationHelper.notify_overtime_submitted(user_id, overtime_id)
```

**Penerima:** Karyawan yang mengajukan

**Pesan:**

- Title: "Pengajuan Lembur Dikirim"
- Message: "Pengajuan lembur Anda telah dikirim dan menunggu persetujuan."

---

### 8. **Pengajuan Lembur Disetujui/Ditolak**

**Trigger:** Atasan/HRD approve atau reject lembur

```python
NotificationHelper.notify_overtime_approval(
    user_id,
    overtime_id,
    approved  # True/False
)
```

**Penerima:** Karyawan yang mengajukan

**Pesan:**

- Title: "Pengajuan Lembur {status}"
- Message: "Pengajuan lembur Anda telah {status}."

---

## 📊 Diagram Flow

### Notifikasi Flow

```
┌──────────────────┐
│  Event Terjadi   │
│  (Presensi,      │
│   Approval, dll) │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Determine       │
│  Recipients      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Create          │
│  Notification    │
│  for Each User   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Save to DB      │
│  (is_read=False) │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  User Loads      │
│  Dashboard       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Fetch           │
│  Unread          │
│  Notifications   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Display Badge   │
│  & List          │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  User Clicks     │
│  Notification    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Mark as Read    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Update Badge    │
└──────────────────┘
```

---

## 🎯 Contoh Skenario

### Skenario 1: Notifikasi Presensi

1. **Karyawan A** melakukan check-in
2. Sistem buat notifikasi: "Presensi Berhasil"
3. Badge notifikasi muncul: **1**
4. Karyawan klik notifikasi → Mark as read
5. Badge hilang

### Skenario 2: Notifikasi Approval Cuti

1. **Karyawan A** mengajukan cuti
2. Notifikasi ke karyawan: "Pengajuan Cuti Dikirim"
3. Notifikasi ke **Atasan B**: "Pengajuan Cuti Baru dari Karyawan A"
4. **Atasan B** approve
5. Notifikasi ke karyawan: "Pengajuan Cuti Disetujui Atasan" (masih menunggu HRD)
6. Notifikasi ke **HRD C**: "Pengajuan Cuti Menunggu Approval HRD"
7. **HRD C** approve
8. Notifikasi ke karyawan: "Pengajuan Cuti Disetujui"

### Skenario 3: Notifikasi Multiple

1. **Karyawan A** punya 5 notifikasi belum dibaca
2. Badge menampilkan: **5**
3. User klik dropdown → Lihat 5 notifikasi
4. User klik "Mark All as Read"
5. Semua notifikasi ditandai sudah dibaca
6. Badge hilang

---

## 📝 Catatan Penting

1. **Notifikasi persistent**: Tersimpan di database
2. **Real-time**: Dibuat saat event terjadi
3. **Role-based**: Dikirim ke user yang relevan
4. **Read/Unread**: Status bisa ditandai sudah dibaca
5. **Related ID**: Link ke record terkait (attendance, leave_request, dll)
6. **Auto-load**: Notifikasi di-fetch saat dropdown dibuka
7. **Security**: User hanya bisa mark read notifikasi sendiri

---

_Dokumen ini akan diperbarui jika ada perubahan pada flow notifikasi._
