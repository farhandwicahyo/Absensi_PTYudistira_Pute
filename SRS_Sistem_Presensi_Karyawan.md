# Sistem Requirement Specification (SRS)

## Sistem Presensi Karyawan Berbasis Website

**Versi Dokumen:** 1.0  
**Tanggal:** 2026  
**Penulis:** Tim Pengembangan  
**Status:** Final

---

## Daftar Isi

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [Specific Requirements](#3-specific-requirements)
4. [System Architecture](#4-system-architecture)
5. [Database Design](#5-database-design)
6. [User Interface Requirements](#6-user-interface-requirements)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [Appendices](#8-appendices)

---

## 1. Introduction

### 1.1 Purpose

Dokumen Sistem Requirement Specification (SRS) ini menjelaskan spesifikasi lengkap untuk Sistem Presensi Karyawan Berbasis Website. Dokumen ini digunakan sebagai acuan dalam perancangan, pengembangan, pengujian, dan implementasi sistem.

### 1.2 Scope

Sistem Presensi Karyawan adalah aplikasi web berbasis Flask yang digunakan untuk:

- Mencatat kehadiran karyawan secara real-time dengan validasi lokasi dan waktu
- Mengelola data karyawan
- Mengelola pengajuan izin, cuti, dan sakit dengan workflow approval
- Mengelola pengajuan lembur
- Menyediakan notifikasi sistem
- Mencatat audit log untuk transparansi dan keamanan

**Batasan Sistem:**

- Sistem hanya dapat diakses melalui web browser
- Presensi memerlukan akses GPS/lokasi dari browser
- Sistem memerlukan koneksi internet untuk mengakses
- Database menggunakan Microsoft SQL Server

### 1.3 Definitions, Acronyms, and Abbreviations

| Istilah         | Definisi                                    |
| --------------- | ------------------------------------------- |
| **SRS**         | Software Requirements Specification         |
| **Admin**       | Administrator sistem dengan akses penuh     |
| **HRD**         | Human Resources Department                  |
| **Check-in**    | Presensi masuk kerja                        |
| **Check-out**   | Presensi pulang kerja                       |
| **Geolocation** | Teknologi untuk menentukan lokasi geografis |
| **Geofencing**  | Teknologi untuk membatasi area presensi     |
| **RBAC**        | Role-Based Access Control                   |
| **MVC**         | Model-View-Controller                       |
| **API**         | Application Programming Interface           |
| **CRUD**        | Create, Read, Update, Delete                |

### 1.4 References

- IEEE Std 830-1998 - IEEE Recommended Practice for Software Requirements Specifications
- Flask Documentation: https://flask.palletsprojects.com/
- SQL Server Documentation: https://docs.microsoft.com/sql/
- HTML5 Geolocation API Specification

### 1.5 Overview

Dokumen ini terorganisir dalam beberapa bagian:

- **Section 1**: Pendahuluan dan definisi
- **Section 2**: Deskripsi keseluruhan sistem
- **Section 3**: Requirement spesifik (fungsional dan non-fungsional)
- **Section 4**: Arsitektur sistem
- **Section 5**: Desain database
- **Section 6**: Requirement user interface
- **Section 7**: Non-functional requirements
- **Section 8**: Appendices

---

## 2. Overall Description

### 2.1 Product Perspective

Sistem Presensi Karyawan adalah sistem standalone yang beroperasi sebagai aplikasi web. Sistem ini berinteraksi dengan:

- **Database**: Microsoft SQL Server untuk penyimpanan data
- **Browser**: Web browser modern yang mendukung HTML5 Geolocation API
- **Server**: Web server Flask (Python)

**Diagram Konteks Sistem:**

```
┌─────────────┐
│   Browser   │
│  (Client)   │
└──────┬──────┘
       │ HTTP/HTTPS
       │
┌──────▼──────────────────┐
│   Flask Application      │
│   (Web Server)           │
└──────┬───────────────────┘
       │ SQL Queries
       │
┌──────▼──────────┐
│  SQL Server      │
│  (Database)      │
└──────────────────┘
```

### 2.2 Product Functions

Sistem menyediakan fungsi-fungsi utama berikut:

1. **Autentikasi dan Autorisasi**

   - Login dan logout
   - Manajemen session
   - Role-based access control (Admin, HRD, Atasan, Karyawan)

2. **Presensi Kehadiran**

   - Check-in dengan validasi lokasi dan waktu
   - Check-out dengan validasi lokasi dan waktu
   - Riwayat presensi
   - Status presensi (hadir, terlambat, pulang cepat, alpha)

3. **Manajemen Data Karyawan**

   - CRUD data karyawan
   - Import/Export data (CSV/Excel)
   - Manajemen hierarki karyawan (supervisor)

4. **Pengajuan Timeoff**

   - Pengajuan oleh karyawan
   - Workflow approval (Atasan → HRD)
   - Upload dokumen pendukung

5. **Pengajuan Lembur**

   - Pengajuan lembur oleh karyawan
   - Approval oleh atasan dan HRD
   - Perhitungan total jam lembur

6. **Notifikasi Sistem**

   - Notifikasi real-time
   - Notifikasi untuk approval
   - Notifikasi presensi

7. **Audit Log**

   - Pencatatan semua aktivitas penting
   - Tracking perubahan data
   - Log keamanan

8. **Dashboard**
   - Statistik sesuai role
   - Ringkasan aktivitas
   - Notifikasi terbaru

### 2.3 User Characteristics

#### 2.3.1 Admin

- **Pengetahuan**: Familiar dengan sistem komputer dan web browser
- **Pengalaman**: Pengalaman menggunakan aplikasi web
- **Tugas**: Mengelola seluruh sistem, data karyawan, dan audit log

#### 2.3.2 HRD

- **Pengetahuan**: Familiar dengan sistem komputer dan web browser
- **Pengalaman**: Pengalaman menggunakan aplikasi web
- **Tugas**: Mengelola data karyawan, approval pengajuan, laporan presensi

#### 2.3.3 Atasan

- **Pengetahuan**: Familiar dengan web browser
- **Pengalaman**: Pengalaman dasar menggunakan aplikasi web
- **Tugas**: Approval pengajuan bawahan, melihat laporan presensi bawahan

#### 2.3.4 Karyawan

- **Pengetahuan**: Familiar dengan web browser dan smartphone
- **Pengalaman**: Pengalaman dasar menggunakan aplikasi web
- **Tugas**: Presensi, pengajuan Timeoff, pengajuan lembur

### 2.4 Constraints

#### 2.4.1 Hardware Constraints

- Server: Minimum 2GB RAM, 10GB storage
- Client: Device dengan GPS capability untuk presensi berbasis lokasi
- Network: Koneksi internet stabil

#### 2.4.2 Software Constraints

- **Server**: Python 3.8+, Flask 3.0+
- **Database**: Microsoft SQL Server dengan ODBC Driver 17
- **Browser**: Browser modern yang mendukung HTML5 Geolocation API (Chrome, Firefox, Edge, Safari)
- **OS**: Windows Server untuk database, Linux/Windows untuk aplikasi

#### 2.4.3 Regulatory Constraints

- Kepatuhan terhadap kebijakan privasi data karyawan
- Audit trail untuk transparansi
- Backup data secara berkala

#### 2.4.4 Interface Constraints

- Sistem harus dapat diakses melalui web browser
- Responsive design untuk mobile dan desktop
- Kompatibilitas dengan berbagai ukuran layar

### 2.5 Assumptions and Dependencies

#### 2.5.1 Assumptions

- Pengguna memiliki akses internet
- Browser pengguna mendukung HTML5 Geolocation API
- Pengguna memberikan izin akses lokasi saat presensi
- SQL Server sudah terinstall dan berjalan
- Koneksi database stabil

#### 2.5.2 Dependencies

- **Flask Framework**: Untuk web application
- **SQLAlchemy**: Untuk ORM database
- **Werkzeug**: Untuk password hashing
- **pyodbc**: Untuk koneksi SQL Server
- **Flowbite/Tailwind CSS**: Untuk UI components
- **HTML5 Geolocation API**: Untuk deteksi lokasi

---

## 3. Specific Requirements

### 3.1 Functional Requirements

#### 3.1.1 Autentikasi dan Autorisasi

**FR-001: Login**

- **ID**: FR-001
- **Prioritas**: High
- **Deskripsi**: Sistem harus menyediakan halaman login untuk autentikasi pengguna
- **Input**: Username/email dan password
- **Proses**:
  1. User memasukkan username/email dan password
  2. Sistem memvalidasi kredensial
  3. Sistem memverifikasi password dengan hash yang tersimpan
  4. Sistem membuat session jika valid
  5. Sistem mencatat last_login dan IP address
- **Output**: Redirect ke dashboard sesuai role
- **Error Handling**:
  - Username/password salah → tampilkan pesan error
  - User tidak aktif → tampilkan pesan error
  - Session expired → redirect ke login

**FR-002: Logout**

- **ID**: FR-002
- **Prioritas**: High
- **Deskripsi**: Sistem harus menyediakan fungsi logout
- **Proses**:
  1. User klik tombol logout
  2. Sistem menghapus session
  3. Sistem redirect ke halaman login
- **Output**: Halaman login

**FR-003: Session Management**

- **ID**: FR-003
- **Prioritas**: High
- **Deskripsi**: Sistem harus mengelola session pengguna
- **Requirement**:
  - Session timeout setelah 8 jam tidak aktif
  - Session disimpan di server
  - Setiap request harus memvalidasi session
- **Error Handling**: Session expired → redirect ke login

**FR-004: Role-Based Access Control**

- **ID**: FR-004
- **Prioritas**: High
- **Deskripsi**: Sistem harus membatasi akses berdasarkan role
- **Roles**:
  - **Admin**: Akses penuh ke semua fitur
  - **HRD**: Akses ke manajemen karyawan, approval, laporan
  - **Atasan**: Akses ke approval bawahan, laporan bawahan
  - **Karyawan**: Akses ke presensi, pengajuan
- **Proses**: Setiap request dicek role pengguna sebelum mengizinkan akses

#### 3.1.2 Presensi Kehadiran

**FR-005: Check-in**

- **ID**: FR-005
- **Prioritas**: High
- **Deskripsi**: Sistem harus menyediakan fungsi check-in untuk presensi masuk
- **Input**:
  - Employee ID (dari session)
  - Latitude dan Longitude (dari GPS)
  - Timestamp (dari server)
- **Proses**:
  1. User klik tombol "Check In"
  2. Browser meminta izin akses lokasi
  3. Sistem mendapatkan koordinat GPS
  4. Sistem memvalidasi:
     - Lokasi dalam radius yang ditentukan (geofencing)
     - Waktu dalam rentang check-in (07:00 - 09:00)
     - Belum ada check-in hari ini
  5. Sistem mendeteksi informasi perangkat (browser, OS, IP)
  6. Sistem menentukan status (hadir/terlambat)
  7. Sistem menyimpan data ke database
  8. Sistem membuat audit log
  9. Sistem membuat notifikasi
- **Output**:
  - Success: Pesan sukses dan update tampilan
  - Error: Pesan error sesuai validasi yang gagal
- **Validasi**:
  - Lokasi harus dalam radius 100 meter dari koordinat kantor
  - Waktu harus antara 07:00 - 09:00
  - Tidak boleh double check-in dalam satu hari
- **Error Handling**:
  - Lokasi di luar radius → "Anda berada di luar area kantor"
  - Waktu di luar rentang → "Waktu check-in tidak valid"
  - Sudah check-in → "Anda sudah melakukan check-in hari ini"
  - GPS tidak tersedia → "Akses lokasi diperlukan untuk presensi"

**FR-006: Check-out**

- **ID**: FR-006
- **Prioritas**: High
- **Deskripsi**: Sistem harus menyediakan fungsi check-out untuk presensi pulang
- **Input**:
  - Employee ID (dari session)
  - Attendance ID (check-in hari ini)
  - Latitude dan Longitude (dari GPS)
  - Timestamp (dari server)
- **Proses**:
  1. User klik tombol "Check Out"
  2. Sistem memvalidasi sudah check-in hari ini
  3. Browser meminta izin akses lokasi
  4. Sistem mendapatkan koordinat GPS
  5. Sistem memvalidasi lokasi dalam radius
  6. Sistem mendeteksi informasi perangkat
  7. Sistem menentukan status (pulang cepat jika sebelum 16:00)
  8. Sistem update data check-out di database
  9. Sistem membuat audit log
  10. Sistem membuat notifikasi
- **Output**:
  - Success: Pesan sukses dan update tampilan
  - Error: Pesan error sesuai validasi yang gagal
- **Validasi**:
  - Harus sudah check-in hari ini
  - Lokasi harus dalam radius kantor
  - Waktu harus setelah jam check-in
- **Error Handling**:
  - Belum check-in → "Anda belum melakukan check-in"
  - Lokasi di luar radius → "Anda berada di luar area kantor"

**FR-007: Riwayat Presensi**

- **ID**: FR-007
- **Prioritas**: Medium
- **Deskripsi**: Sistem harus menampilkan riwayat presensi
- **Fitur**:
  - Filter berdasarkan tanggal
  - Tampilkan status presensi
  - Tampilkan waktu check-in dan check-out
  - Export data (untuk HRD/Admin)
- **Akses**:
  - Karyawan: Hanya melihat presensi sendiri
  - Atasan: Melihat presensi bawahan
  - HRD/Admin: Melihat semua presensi

**FR-008: Status Presensi**

- **ID**: FR-008
- **Prioritas**: High
- **Deskripsi**: Sistem harus menentukan status presensi otomatis
- **Status**:
  - **Hadir**: Check-in tepat waktu (sebelum 09:00)
  - **Terlambat**: Check-in setelah 09:00
  - **Pulang Cepat**: Check-out sebelum 16:00
  - **Alpha**: Tidak ada check-in hari itu
- **Proses**: Status ditentukan otomatis saat check-in/check-out

#### 3.1.3 Manajemen Data Karyawan

**FR-009: Tambah Karyawan**

- **ID**: FR-009
- **Prioritas**: High
- **Deskripsi**: Admin/HRD dapat menambah data karyawan baru
- **Input**:
  - NIK (unique)
  - Nama lengkap
  - Email (unique)
  - Nomor HP
  - Jabatan
  - Divisi
  - Atasan langsung (supervisor)
  - Tanggal masuk kerja
- **Validasi**:
  - NIK harus unique
  - Email harus unique dan valid format
  - Semua field wajib diisi
- **Proses**:
  1. Admin/HRD mengisi form
  2. Sistem memvalidasi data
  3. Sistem menyimpan ke database
  4. Sistem membuat audit log
- **Output**: Pesan sukses dan redirect ke daftar karyawan

**FR-010: Edit Karyawan**

- **ID**: FR-010
- **Prioritas**: High
- **Deskripsi**: Admin/HRD dapat mengedit data karyawan
- **Proses**: Similar dengan tambah karyawan, dengan validasi data existing
- **Output**: Pesan sukses dan update tampilan

**FR-011: Hapus/Nonaktifkan Karyawan**

- **ID**: FR-011
- **Prioritas**: Medium
- **Deskripsi**: Admin/HRD dapat menghapus atau menonaktifkan karyawan
- **Proses**:
  1. Admin/HRD klik tombol hapus/nonaktifkan
  2. Sistem konfirmasi
  3. Sistem update status karyawan menjadi "nonaktif"
  4. Sistem membuat audit log
- **Note**: Data tidak dihapus, hanya diubah statusnya

**FR-012: Import Data Karyawan**

- **ID**: FR-012
- **Prioritas**: Medium
- **Deskripsi**: Admin/HRD dapat import data karyawan dari file CSV/Excel
- **Format File**: CSV dengan kolom: NIK, Nama, Email, Phone, Position, Division, Supervisor NIK, Hire Date
- **Proses**:
  1. Admin/HRD upload file
  2. Sistem memvalidasi format file
  3. Sistem membaca dan memvalidasi data
  4. Sistem menyimpan data ke database
  5. Sistem membuat audit log
- **Error Handling**:
  - Format file tidak valid → tampilkan error
  - Data duplikat → skip atau tampilkan warning

**FR-013: Export Data Karyawan**

- **ID**: FR-013
- **Prioritas**: Medium
- **Deskripsi**: Admin/HRD dapat export data karyawan ke file CSV/Excel
- **Proses**:
  1. Admin/HRD klik tombol export
  2. Sistem mengambil data dari database
  3. Sistem generate file CSV/Excel
  4. Sistem download file ke client

#### 3.1.4 Pengajuan Timeoff

**FR-014: Pengajuan Timeoff**

- **ID**: FR-014
- **Prioritas**: High
- **Deskripsi**: Karyawan dapat mengajukan izin, cuti, atau sakit
- **Input**:
  - Jenis pengajuan (Timeoff)
  - Tanggal mulai
  - Tanggal selesai
  - Alasan
  - Dokumen pendukung (optional)
- **Validasi**:
  - Tanggal mulai tidak boleh lebih dari tanggal selesai
  - Tanggal tidak boleh di masa lalu (untuk cuti)
  - File upload maksimal 5MB
  - Format file: PDF, PNG, JPG, DOC, DOCX
- **Proses**:
  1. Karyawan mengisi form
  2. Sistem memvalidasi data
  3. Sistem menyimpan pengajuan dengan status "menunggu"
  4. Sistem membuat notifikasi untuk atasan
  5. Sistem membuat audit log
- **Output**: Pesan sukses dan redirect ke daftar pengajuan

**FR-015: Approval Workflow**

- **ID**: FR-015
- **Prioritas**: High
- **Deskripsi**: Sistem harus menyediakan workflow approval untuk pengajuan
- **Workflow**:
  - **Cuti**: Karyawan → Atasan → HRD → Disetujui
  - **Izin**: Karyawan → Atasan → HRD → Disetujui
  - **Sakit**: Karyawan → Atasan → HRD → Disetujui
- **Proses Approval**:
  1. Atasan menerima notifikasi
  2. Atasan review pengajuan
  3. Atasan approve/reject
  4. Jika approve, notifikasi ke HRD
  5. HRD review dan approve/reject
  6. Jika approve, status menjadi "disetujui" dan notifikasi ke karyawan
  7. Jika reject, status menjadi "ditolak" dengan alasan
- **Output**: Update status dan notifikasi

**FR-016: Lihat Pengajuan**

- **ID**: FR-016
- **Prioritas**: Medium
- **Deskripsi**: User dapat melihat daftar pengajuan sesuai role
- **Akses**:
  - Karyawan: Hanya pengajuan sendiri
  - Atasan: Pengajuan bawahan
  - HRD/Admin: Semua pengajuan
- **Filter**: Status, jenis pengajuan, tanggal

#### 3.1.5 Pengajuan Lembur

**FR-017: Pengajuan Lembur**

- **ID**: FR-017
- **Prioritas**: High
- **Deskripsi**: Karyawan dapat mengajukan lembur
- **Input**:
  - Tanggal lembur
  - Jam mulai
  - Jam selesai
  - Alasan
- **Validasi**:
  - Jam selesai harus setelah jam mulai
  - Total jam lembur dihitung otomatis
- **Proses**:
  1. Karyawan mengisi form
  2. Sistem menghitung total jam lembur
  3. Sistem menyimpan dengan status "menunggu"
  4. Sistem membuat notifikasi untuk atasan
  5. Sistem membuat audit log
- **Output**: Pesan sukses

**FR-018: Approval Lembur**

- **ID**: FR-018
- **Prioritas**: High
- **Deskripsi**: Atasan dan HRD dapat approve/reject pengajuan lembur
- **Workflow**: Similar dengan approval Timeoff
- **Proses**: Similar dengan FR-015

#### 3.1.6 Notifikasi Sistem

**FR-019: Notifikasi Real-time**

- **ID**: FR-019
- **Prioritas**: Medium
- **Deskripsi**: Sistem harus menyediakan notifikasi untuk berbagai event
- **Jenis Notifikasi**:
  - Presensi berhasil/gagal
  - Pengajuan baru untuk approval
  - Status approval (disetujui/ditolak)
  - Pengingat presensi
- **Proses**:
  1. Event terjadi (presensi, pengajuan, approval)
  2. Sistem membuat notifikasi
  3. Sistem menyimpan ke database
  4. Sistem menampilkan di dashboard
- **Output**: Badge notifikasi di UI

**FR-020: Mark Notifikasi as Read**

- **ID**: FR-020
- **Prioritas**: Low
- **Deskripsi**: User dapat menandai notifikasi sebagai sudah dibaca
- **Proses**: User klik notifikasi → sistem update status menjadi "read"

#### 3.1.7 Audit Log

**FR-021: Audit Log**

- **ID**: FR-021
- **Prioritas**: High
- **Deskripsi**: Sistem harus mencatat semua aktivitas penting
- **Aktivitas yang Dicatat**:
  - Login dan logout
  - Presensi (check-in/check-out)
  - CRUD data karyawan
  - Pengajuan dan approval
  - Perubahan data penting
- **Informasi yang Dicatat**:
  - User ID
  - Aktivitas
  - Timestamp
  - IP Address
  - Detail perubahan (untuk update/delete)
- **Akses**: Hanya Admin yang dapat melihat audit log
- **Filter**: Tanggal, user, aktivitas

#### 3.1.8 Dashboard

**FR-022: Dashboard**

- **ID**: FR-022
- **Prioritas**: High
- **Deskripsi**: Sistem harus menyediakan dashboard sesuai role
- **Dashboard Karyawan**:
  - Status presensi hari ini
  - Pengajuan pending
  - Lembur pending
  - Notifikasi terbaru
- **Dashboard Atasan**:
  - Jumlah bawahan
  - Pengajuan pending untuk approval
  - Statistik presensi bawahan
- **Dashboard HRD**:
  - Total karyawan
  - Presensi hari ini
  - Pengajuan pending
  - Statistik presensi
- **Dashboard Admin**:
  - Total karyawan
  - Presensi hari ini
  - Pengajuan pending
  - Aktivitas terbaru (audit log)

### 3.2 Non-Functional Requirements

#### 3.2.1 Performance Requirements

**NFR-001: Response Time**

- **ID**: NFR-001
- **Prioritas**: High
- **Requirement**:
  - Halaman harus load dalam waktu maksimal 3 detik
  - Query database harus selesai dalam waktu maksimal 1 detik
  - Presensi harus tersimpan dalam waktu maksimal 2 detik

**NFR-002: Throughput**

- **ID**: NFR-002
- **Prioritas**: Medium
- **Requirement**: Sistem harus dapat menangani minimal 100 concurrent users

**NFR-003: Scalability**

- **ID**: NFR-003
- **Prioritas**: Medium
- **Requirement**: Sistem harus dapat diskalakan untuk menambah jumlah pengguna

#### 3.2.2 Security Requirements

**NFR-004: Password Security**

- **ID**: NFR-004
- **Prioritas**: High
- **Requirement**:
  - Password harus di-hash menggunakan Werkzeug (PBKDF2)
  - Password tidak boleh disimpan dalam plain text
  - Minimum panjang password: 6 karakter

**NFR-005: Session Security**

- **ID**: NFR-005
- **Prioritas**: High
- **Requirement**:
  - Session harus expire setelah 8 jam tidak aktif
  - Session ID harus unik dan tidak dapat ditebak
  - Session harus dihapus saat logout

**NFR-006: Data Encryption**

- **ID**: NFR-006
- **Prioritas**: Medium
- **Requirement**:
  - Data sensitif harus dienkripsi saat transit (HTTPS)
  - Password harus di-hash di database

**NFR-007: Access Control**

- **ID**: NFR-007
- **Prioritas**: High
- **Requirement**:
  - Setiap request harus memvalidasi role pengguna
  - Pengguna tidak dapat mengakses fitur di luar role mereka
  - Audit log untuk semua akses

#### 3.2.3 Reliability Requirements

**NFR-008: Availability**

- **ID**: NFR-008
- **Prioritas**: High
- **Requirement**: Sistem harus tersedia 99% dari waktu operasional (8 jam kerja)

**NFR-009: Error Handling**

- **ID**: NFR-009
- **Prioritas**: High
- **Requirement**:
  - Sistem harus menangani error dengan graceful
  - Error message harus informatif untuk user
  - Error tidak boleh mengekspos informasi sensitif

**NFR-010: Data Backup**

- **ID**: NFR-010
- **Prioritas**: High
- **Requirement**:
  - Database harus di-backup secara berkala (harian)
  - Backup harus disimpan di lokasi terpisah
  - Proses restore harus dapat dilakukan dalam waktu maksimal 1 jam

#### 3.2.4 Usability Requirements

**NFR-011: User Interface**

- **ID**: NFR-011
- **Prioritas**: High
- **Requirement**:
  - Interface harus user-friendly dan intuitif
  - Menggunakan Flowbite/Tailwind CSS untuk konsistensi
  - Responsive design untuk mobile dan desktop

**NFR-012: Accessibility**

- **ID**: NFR-012
- **Prioritas**: Medium
- **Requirement**:
  - Interface harus dapat diakses melalui berbagai browser
  - Kontras warna harus cukup untuk readability

#### 3.2.5 Maintainability Requirements

**NFR-013: Code Quality**

- **ID**: NFR-013
- **Prioritas**: Medium
- **Requirement**:
  - Kode harus mengikuti best practices
  - Menggunakan arsitektur MVC
  - Kode harus terdokumentasi

**NFR-014: Logging**

- **ID**: NFR-014
- **Prioritas**: Medium
- **Requirement**:
  - Sistem harus mencatat log untuk debugging
  - Log harus dapat diakses oleh admin

---

## 4. System Architecture

### 4.1 Architecture Overview

Sistem menggunakan arsitektur **MVC (Model-View-Controller)**:

```
┌─────────────────────────────────────────┐
│              View Layer                  │
│  (HTML Templates + JavaScript)          │
└──────────────┬──────────────────────────┘
               │ HTTP Request/Response
┌──────────────▼──────────────────────────┐
│         Controller Layer                │
│  (Flask Routes + Business Logic)       │
└──────────────┬──────────────────────────┘
               │ ORM Queries
┌──────────────▼──────────────────────────┐
│          Model Layer                    │
│  (SQLAlchemy Models + Database)        │
└─────────────────────────────────────────┘
```

### 4.2 Technology Stack

- **Backend Framework**: Flask 3.0.0 (Python)
- **Database**: Microsoft SQL Server
- **ORM**: SQLAlchemy 3.1.1
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Flowbite (Tailwind CSS)
- **Password Hashing**: Werkzeug 3.0.1
- **Database Driver**: pyodbc 5.0.1

### 4.3 Directory Structure

```
Absensi_PTYudistira_Pute/
├── app.py                    # Main application entry point
├── config.py                # Configuration
├── init_db.py               # Database initialization
├── requirements.txt         # Python dependencies
├── models/                  # Database models
│   ├── user.py
│   ├── employee.py
│   ├── attendance.py
│   ├── leave_request.py
│   ├── overtime.py
│   ├── notification.py
│   └── audit_log.py
├── controllers/             # Business logic
│   ├── auth_controller.py
│   ├── dashboard_controller.py
│   ├── attendance_controller.py
│   ├── employee_controller.py
│   ├── leave_controller.py
│   ├── overtime_controller.py
│   ├── notification_controller.py
│   └── audit_controller.py
├── utils/                   # Utility functions
│   ├── decorators.py
│   ├── audit_logger.py
│   ├── geolocation.py
│   ├── device_info.py
│   └── notification_helper.py
├── templates/              # HTML templates
│   ├── base.html
│   ├── auth/
│   ├── dashboard/
│   ├── attendance/
│   ├── employee/
│   ├── leave/
│   ├── overtime/
│   └── audit/
└── uploads/                # File uploads
```

---

## 5. Database Design

### 5.1 Entity Relationship Diagram

```
┌─────────────┐         ┌──────────────┐
│    User     │────────▶│   Employee   │
└─────────────┘         └──────┬───────┘
                                │
                                │
                    ┌───────────┼───────────┐
                    │           │           │
            ┌───────▼───┐  ┌────▼────┐  ┌──▼──────┐
            │Attendance │  │  Leave   │  │Overtime │
            │           │  │ Request  │  │         │
            └───────────┘  └──────────┘  └─────────┘
                    │
            ┌───────▼───────┐
            │ Notification │
            └──────────────┘
                    │
            ┌───────▼───────┐
            │  Audit Log    │
            └───────────────┘
```

### 5.2 Database Tables

#### 5.2.1 Table: users

- **Purpose**: Menyimpan data user untuk autentikasi
- **Primary Key**: id
- **Fields**:
  - id (INT, PK, Auto Increment)
  - username (VARCHAR(50), Unique, Not Null)
  - email (VARCHAR(100), Unique, Not Null)
  - password_hash (VARCHAR(255), Not Null)
  - role (VARCHAR(20), Not Null) - admin, hrd, atasan, karyawan
  - employee_id (INT, FK → employees.id, Nullable)
  - is_active (BOOLEAN, Default: True)
  - last_login (DATETIME, Nullable)
  - last_login_ip (VARCHAR(45), Nullable)
  - created_at (DATETIME, Default: Current Timestamp)
  - updated_at (DATETIME, Default: Current Timestamp)

#### 5.2.2 Table: employees

- **Purpose**: Menyimpan data karyawan
- **Primary Key**: id
- **Fields**:
  - id (INT, PK, Auto Increment)
  - nik (VARCHAR(20), Unique, Not Null)
  - full_name (VARCHAR(100), Not Null)
  - email (VARCHAR(100), Not Null)
  - phone (VARCHAR(20), Nullable)
  - position (VARCHAR(50), Not Null)
  - division (VARCHAR(50), Not Null)
  - supervisor_id (INT, FK → employees.id, Nullable)
  - status (VARCHAR(20), Default: 'aktif')
  - hire_date (DATE, Nullable)
  - created_at (DATETIME, Default: Current Timestamp)
  - updated_at (DATETIME, Default: Current Timestamp)

#### 5.2.3 Table: attendances

- **Purpose**: Menyimpan data presensi
- **Primary Key**: id
- **Fields**:
  - id (INT, PK, Auto Increment)
  - employee_id (INT, FK → employees.id, Not Null)
  - attendance_date (DATE, Not Null, Default: Current Date)
  - check_in_time (DATETIME, Nullable)
  - check_out_time (DATETIME, Nullable)
  - check_in_latitude (FLOAT, Nullable)
  - check_in_longitude (FLOAT, Nullable)
  - check_out_latitude (FLOAT, Nullable)
  - check_out_longitude (FLOAT, Nullable)
  - check_in_ip (VARCHAR(45), Nullable)
  - check_out_ip (VARCHAR(45), Nullable)
  - check_in_browser (VARCHAR(100), Nullable)
  - check_out_browser (VARCHAR(100), Nullable)
  - check_in_os (VARCHAR(50), Nullable)
  - check_out_os (VARCHAR(50), Nullable)
  - status (VARCHAR(20), Default: 'hadir')
  - notes (TEXT, Nullable)
  - created_at (DATETIME, Default: Current Timestamp)
  - updated_at (DATETIME, Default: Current Timestamp)

#### 5.2.4 Table: leave_requests

- **Purpose**: Menyimpan pengajuan Timeoff
- **Primary Key**: id
- **Fields**:
  - id (INT, PK, Auto Increment)
  - employee_id (INT, FK → employees.id, Not Null)
  - leave_type (VARCHAR(20), Not Null) - izin, cuti, sakit
  - start_date (DATE, Not Null)
  - end_date (DATE, Not Null)
  - reason (TEXT, Not Null)
  - attachment_path (VARCHAR(255), Nullable)
  - status (VARCHAR(20), Default: 'menunggu')
  - supervisor_approval (BOOLEAN, Default: False)
  - supervisor_approval_date (DATETIME, Nullable)
  - supervisor_id (INT, FK → employees.id, Nullable)
  - hrd_approval (BOOLEAN, Default: False)
  - hrd_approval_date (DATETIME, Nullable)
  - hrd_id (INT, FK → users.id, Nullable)
  - rejection_reason (TEXT, Nullable)
  - created_at (DATETIME, Default: Current Timestamp)
  - updated_at (DATETIME, Default: Current Timestamp)

#### 5.2.5 Table: overtimes

- **Purpose**: Menyimpan pengajuan lembur
- **Primary Key**: id
- **Fields**:
  - id (INT, PK, Auto Increment)
  - employee_id (INT, FK → employees.id, Not Null)
  - overtime_date (DATE, Not Null)
  - start_time (TIME, Not Null)
  - end_time (TIME, Not Null)
  - total_hours (FLOAT, Not Null)
  - reason (TEXT, Not Null)
  - status (VARCHAR(20), Default: 'menunggu')
  - supervisor_approval (BOOLEAN, Default: False)
  - supervisor_approval_date (DATETIME, Nullable)
  - supervisor_id (INT, FK → employees.id, Nullable)
  - hrd_approval (BOOLEAN, Default: False)
  - hrd_approval_date (DATETIME, Nullable)
  - hrd_id (INT, FK → users.id, Nullable)
  - rejection_reason (TEXT, Nullable)
  - created_at (DATETIME, Default: Current Timestamp)
  - updated_at (DATETIME, Default: Current Timestamp)

#### 5.2.6 Table: notifications

- **Purpose**: Menyimpan notifikasi sistem
- **Primary Key**: id
- **Fields**:
  - id (INT, PK, Auto Increment)
  - user_id (INT, FK → users.id, Not Null)
  - title (VARCHAR(255), Not Null)
  - message (TEXT, Not Null)
  - type (VARCHAR(50), Not Null)
  - is_read (BOOLEAN, Default: False)
  - created_at (DATETIME, Default: Current Timestamp)

#### 5.2.7 Table: audit_logs

- **Purpose**: Menyimpan log aktivitas sistem
- **Primary Key**: id
- **Fields**:
  - id (INT, PK, Auto Increment)
  - user_id (INT, FK → users.id, Nullable)
  - activity (VARCHAR(100), Not Null)
  - entity_type (VARCHAR(50), Nullable)
  - entity_id (INT, Nullable)
  - details (TEXT, Nullable)
  - ip_address (VARCHAR(45), Nullable)
  - created_at (DATETIME, Default: Current Timestamp)

### 5.3 Indexes

- **users**: username (unique), email (unique)
- **employees**: nik (unique), email
- **attendances**: employee_id, attendance_date (composite index)
- **leave_requests**: employee_id, status
- **overtimes**: employee_id, status
- **notifications**: user_id, is_read
- **audit_logs**: user_id, created_at

---

## 6. User Interface Requirements

### 6.1 Design Principles

- **Consistency**: Menggunakan Flowbite/Tailwind CSS untuk konsistensi UI
- **Responsiveness**: Design harus responsive untuk mobile dan desktop
- **Accessibility**: Kontras warna yang cukup, font size yang readable
- **User-Friendly**: Interface intuitif dan mudah digunakan

### 6.2 Page Requirements

#### 6.2.1 Login Page

- Form login dengan username/email dan password
- Tombol "Login"
- Link "Lupa Password" (opsional)
- Pesan error jika login gagal

#### 6.2.2 Dashboard

- Statistik cards sesuai role
- Notifikasi terbaru
- Quick actions
- Menu navigasi sidebar

#### 6.2.3 Presensi Page

- Tombol "Check In" dan "Check Out"
- Status presensi hari ini
- Riwayat presensi (tabel)
- Filter tanggal

#### 6.2.4 Data Karyawan Page

- Tabel daftar karyawan
- Tombol "Tambah Karyawan"
- Tombol "Edit" dan "Hapus" per row
- Tombol "Import" dan "Export"
- Search dan filter

#### 6.2.5 Pengajuan Timeoff Page

- Tabel daftar pengajuan
- Tombol "Ajukan" (untuk karyawan)
- Tombol "Approve/Reject" (untuk atasan/HRD)
- Filter status dan jenis

#### 6.2.6 Pengajuan Lembur Page

- Tabel daftar pengajuan lembur
- Tombol "Ajukan" (untuk karyawan)
- Tombol "Approve/Reject" (untuk atasan/HRD)
- Filter status

#### 6.2.7 Audit Log Page

- Tabel audit log
- Filter tanggal, user, aktivitas
- Pagination

### 6.3 Responsive Design

- **Desktop**: Layout dengan sidebar
- **Tablet**: Layout dengan collapsible sidebar
- **Mobile**: Hamburger menu untuk navigasi

---

## 7. Non-Functional Requirements (Detailed)

### 7.1 Performance

- **Response Time**: Maksimal 3 detik untuk load halaman
- **Database Query**: Maksimal 1 detik
- **Concurrent Users**: Minimal 100 users bersamaan
- **Throughput**: Minimal 50 requests per detik

### 7.2 Security

- **Password**: Hash menggunakan PBKDF2 (Werkzeug)
- **Session**: Secure session dengan timeout 8 jam
- **HTTPS**: Wajib untuk production (opsional untuk development)
- **SQL Injection**: Prevention melalui SQLAlchemy ORM
- **XSS Protection**: Input validation dan sanitization
- **CSRF Protection**: Token-based protection

### 7.3 Reliability

- **Uptime**: 99% availability selama jam kerja
- **Error Recovery**: Graceful error handling
- **Data Integrity**: Transaction support untuk operasi kritis
- **Backup**: Daily backup dengan retention 30 hari

### 7.4 Usability

- **Learning Curve**: User dapat menggunakan sistem dalam waktu maksimal 15 menit
- **Help Documentation**: Tersedia di setiap halaman (tooltip/help text)
- **Error Messages**: Jelas dan informatif
- **Multi-language**: Support Bahasa Indonesia (primary)

### 7.5 Maintainability

- **Code Documentation**: Setiap fungsi terdokumentasi
- **Version Control**: Menggunakan Git
- **Testing**: Unit test untuk critical functions
- **Logging**: Comprehensive logging untuk debugging

---

## 8. Appendices

### 8.1 Glossary

| Istilah         | Definisi                                                    |
| --------------- | ----------------------------------------------------------- |
| **Check-in**    | Proses presensi masuk kerja                                 |
| **Check-out**   | Proses presensi pulang kerja                                |
| **Geofencing**  | Teknologi untuk membatasi area presensi                     |
| **Geolocation** | Teknologi untuk menentukan lokasi geografis                 |
| **RBAC**        | Role-Based Access Control - kontrol akses berdasarkan peran |
| **Session**     | Status login pengguna yang aktif                            |
| **Workflow**    | Alur proses bisnis yang terstruktur                         |

### 8.2 Acronyms

- **SRS**: Software Requirements Specification
- **MVC**: Model-View-Controller
- **API**: Application Programming Interface
- **CRUD**: Create, Read, Update, Delete
- **RBAC**: Role-Based Access Control
- **GPS**: Global Positioning System
- **HTTP**: Hypertext Transfer Protocol
- **HTTPS**: Hypertext Transfer Protocol Secure
- **ORM**: Object-Relational Mapping
- **SQL**: Structured Query Language
- **UI**: User Interface
- **UX**: User Experience

### 8.3 References

1. IEEE Std 830-1998 - IEEE Recommended Practice for Software Requirements Specifications
2. Flask Documentation: https://flask.palletsprojects.com/
3. SQLAlchemy Documentation: https://www.sqlalchemy.org/
4. Microsoft SQL Server Documentation: https://docs.microsoft.com/sql/
5. HTML5 Geolocation API: https://www.w3.org/TR/geolocation-API/
6. Flowbite Documentation: https://flowbite.com/
7. Tailwind CSS Documentation: https://tailwindcss.com/

### 8.4 Revision History

| Versi | Tanggal | Penulis          | Deskripsi Perubahan |
| ----- | ------- | ---------------- | ------------------- |
| 1.0   | 2026    | Tim Pengembangan | Initial release     |

---

**End of Document**
