# Alur Approval Pengajuan Izin, Cuti, dan Sakit

Dokumen ini menjelaskan alur approval untuk pengajuan izin, cuti, dan sakit dalam sistem presensi.

---

## 📋 Alur Approval

### 1. **CUTI** (Wajib Approval 2 Tahap)

```
Karyawan Mengajukan Cuti
    ↓
Status: "menunggu" / Tahap: "menunggu_atasan"
    ↓
Atasan Review & Approve
    ↓
Status: "menunggu_hrd" / Tahap: "menunggu_hrd"
    ↓
HRD/Admin Review & Approve
    ↓
Status: "disetujui" / Tahap: "disetujui"
```

**Ketentuan:**
- ✅ **Wajib** approval dari atasan terlebih dahulu
- ✅ Setelah atasan approve, **wajib** approval dari HRD/Admin
- ❌ HRD/Admin **tidak bisa** langsung approve tanpa approval atasan
- ✅ Jika karyawan tidak punya atasan, HRD/Admin bisa langsung approve

---

### 2. **IZIN** (Fleksibel)

```
Karyawan Mengajukan Izin
    ↓
Status: "menunggu" / Tahap: "menunggu_atasan" (jika ada atasan)
    ↓
Atasan Review & Approve (jika ada)
    ↓
Status: "disetujui" / Tahap: "disetujui"
```

**Ketentuan:**
- ✅ Jika ada atasan, perlu approval atasan
- ✅ Setelah atasan approve, langsung **disetujui** (tidak perlu HRD)
- ✅ Jika tidak ada atasan, HRD/Admin bisa langsung approve

---

### 3. **SAKIT** (Fleksibel)

```
Karyawan Mengajukan Sakit
    ↓
Status: "menunggu" / Tahap: "menunggu_atasan" (jika ada atasan)
    ↓
Atasan Review & Approve (jika ada)
    ↓
Status: "disetujui" / Tahap: "disetujui"
```

**Ketentuan:**
- ✅ Jika ada atasan, perlu approval atasan
- ✅ Setelah atasan approve, langsung **disetujui** (tidak perlu HRD)
- ✅ Jika tidak ada atasan, HRD/Admin bisa langsung approve

---

## 🔔 Notifikasi

### Saat Pengajuan Dibuat
1. **Karyawan** menerima notifikasi: "Pengajuan [jenis] Dikirim"
2. **Atasan** (jika ada) menerima notifikasi: "Pengajuan [jenis] Baru dari [nama karyawan]"

### Saat Atasan Approve
1. **Karyawan** menerima notifikasi:
   - **Cuti**: "Pengajuan Cuti Disetujui Atasan" (masih menunggu HRD)
   - **Izin/Sakit**: "Pengajuan [jenis] Disetujui"
2. **HRD/Admin** (untuk cuti) menerima notifikasi: "Pengajuan Cuti Menunggu Approval HRD"

### Saat HRD/Admin Approve
1. **Karyawan** menerima notifikasi: "Pengajuan [jenis] Disetujui"

### Saat Ditolak
1. **Karyawan** menerima notifikasi: "Pengajuan [jenis] Ditolak" dengan alasan

---

## 👥 Siapa Bisa Approve?

### **Atasan**
- ✅ Bisa approve pengajuan dari **bawahan langsung** saja
- ✅ Bisa approve: Izin, Cuti, Sakit
- ✅ Untuk **Cuti**: Setelah approve, status menjadi "menunggu_hrd"
- ✅ Untuk **Izin/Sakit**: Setelah approve, langsung "disetujui"

### **HRD**
- ✅ Bisa approve semua pengajuan
- ✅ Untuk **Cuti**: Hanya bisa approve jika atasan sudah approve
- ✅ Untuk **Izin/Sakit**: Bisa langsung approve jika tidak ada atasan

### **Admin**
- ✅ Bisa approve semua pengajuan
- ✅ Untuk **Cuti**: Hanya bisa approve jika atasan sudah approve
- ✅ Untuk **Izin/Sakit**: Bisa langsung approve jika tidak ada atasan

---

## 📊 Status dan Tahap Approval

| Status Database | Tahap Approval | Deskripsi |
|----------------|----------------|-----------|
| `menunggu` | `menunggu_atasan` | Menunggu approval atasan |
| `menunggu_hrd` | `menunggu_hrd` | Atasan sudah approve, menunggu HRD (hanya untuk cuti) |
| `disetujui` | `disetujui` | Sudah disetujui semua pihak |
| `ditolak` | `ditolak` | Ditolak oleh atasan atau HRD |

---

## 🎯 Contoh Skenario

### Skenario 1: Cuti dengan Atasan
1. **Karyawan A** mengajukan cuti
2. Status: `menunggu` → Tahap: `menunggu_atasan`
3. **Atasan B** melihat pengajuan dan approve
4. Status: `menunggu_hrd` → Tahap: `menunggu_hrd`
5. **HRD C** melihat pengajuan dan approve
6. Status: `disetujui` → Tahap: `disetujui`

### Skenario 2: Izin dengan Atasan
1. **Karyawan A** mengajukan izin
2. Status: `menunggu` → Tahap: `menunggu_atasan`
3. **Atasan B** melihat pengajuan dan approve
4. Status: `disetujui` → Tahap: `disetujui` ✅ (langsung selesai)

### Skenario 3: Cuti tanpa Atasan
1. **Karyawan A** mengajukan cuti (tidak punya atasan)
2. Status: `menunggu` → Tahap: `menunggu_approval`
3. **HRD B** bisa langsung approve
4. Status: `disetujui` → Tahap: `disetujui`

### Skenario 4: HRD Coba Approve Cuti Sebelum Atasan
1. **Karyawan A** mengajukan cuti
2. Status: `menunggu` → Tahap: `menunggu_atasan`
3. **HRD B** mencoba approve → ❌ **DITOLAK** dengan pesan: "Pengajuan cuti harus disetujui oleh atasan terlebih dahulu"

---

## 🔒 Validasi dan Keamanan

1. **Validasi Atasan**
   - Atasan hanya bisa approve pengajuan dari bawahan langsung
   - Sistem mengecek `leave_request.supervisor_id == session.employee_id`

2. **Validasi Cuti**
   - HRD/Admin tidak bisa approve cuti jika atasan belum approve
   - Sistem mengecek `supervisor_approval == True` untuk cuti

3. **Validasi Status**
   - Hanya pengajuan dengan status `menunggu` atau `menunggu_hrd` yang bisa di-approve
   - Pengajuan yang sudah `disetujui` atau `ditolak` tidak bisa diubah

---

## 📝 Catatan Penting

1. **Cuti** adalah jenis pengajuan yang paling ketat, memerlukan 2 tahap approval
2. **Izin dan Sakit** lebih fleksibel, hanya perlu 1 tahap approval (dari atasan jika ada)
3. Jika karyawan **tidak punya atasan**, HRD/Admin bisa langsung approve semua jenis pengajuan
4. Semua aktivitas approval dicatat di **Audit Log**
5. Notifikasi otomatis dikirim ke semua pihak yang terlibat

---

*Dokumen ini akan diperbarui jika ada perubahan alur approval.*
