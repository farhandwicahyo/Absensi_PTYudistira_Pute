# Sistem Presensi Karyawan Berbasis Website

Dokumen ini menjelaskan spesifikasi fitur dan kebutuhan sistem presensi karyawan berbasis website yang akan digunakan sebagai acuan dalam perancangan dan pengembangan sistem.

---

## 1. Login dan Hak Akses Pengguna

Fitur login digunakan untuk membatasi akses sistem berdasarkan peran (role) pengguna.

### 1.1 Jenis Pengguna

* **Admin**: Mengelola seluruh sistem
* **HRD**: Mengelola data karyawan dan laporan presensi
* **Atasan**: Menyetujui izin, cuti, dan lembur
* **Karyawan**: Melakukan presensi dan pengajuan

### 1.2 Fitur Login

* Input username/email dan password
* Validasi data pengguna
* Enkripsi password (hash)
* Session management dan logout otomatis
* Reset password
* Riwayat login (waktu, IP address, perangkat)

---

## 2. Presensi Kehadiran (Check-in & Check-out)

Fitur utama untuk mencatat kehadiran karyawan secara real-time.

### 2.1 Presensi Masuk (Check-in)

* Presensi sesuai jam kerja
* Validasi jam server
* Tidak dapat presensi ganda dalam satu hari

### 2.2 Presensi Pulang (Check-out)

* Hanya dapat dilakukan setelah check-in
* Mencatat jam pulang kerja

### 2.3 Status Presensi

* Hadir
* Terlambat
* Pulang cepat
* Tidak hadir (alpha)

---

## 3. Presensi Berbasis Lokasi (Geolocation)

Fitur untuk memastikan presensi dilakukan di lokasi yang ditentukan.

### 3.1 Deteksi Lokasi

* Menggunakan HTML5 Geolocation API
* Koordinat latitude dan longitude

### 3.2 Validasi Lokasi

* Radius lokasi (geofencing)
* Presensi ditolak jika di luar radius
* Dukungan multi lokasi kantor

---

## 4. Presensi Berbasis Waktu dan Perangkat

Digunakan untuk mencegah manipulasi presensi.

### 4.1 Validasi Waktu

* Presensi hanya dapat dilakukan pada jam tertentu
* Menggunakan jam server

### 4.2 Informasi Perangkat

* Browser
* Sistem operasi
* IP address

---

## 5. Manajemen Data Karyawan

Digunakan oleh Admin atau HRD untuk mengelola data karyawan.

### 5.1 Data Karyawan

* ID/NIK karyawan
* Nama lengkap
* Email dan nomor HP
* Jabatan dan divisi
* Status karyawan (aktif/nonaktif)

### 5.2 Pengelolaan Data

* Tambah, ubah, hapus data
* Import dan export data (Excel/CSV)
* Riwayat perubahan data

---

## 6. Pengajuan Izin, Cuti, dan Sakit

Fitur untuk mengelola ketidakhadiran karyawan secara resmi.

### 6.1 Form Pengajuan

* Jenis pengajuan (izin, cuti, sakit)
* Tanggal mulai dan selesai
* Alasan pengajuan

### 6.2 Persetujuan

* Alur persetujuan: Karyawan → Atasan → HRD
* Status: menunggu, disetujui, ditolak
* Upload bukti pendukung

---

## 7. Lembur

Fitur untuk mencatat jam kerja di luar jam normal.

### 7.1 Pengajuan Lembur

* Tanggal dan jam lembur
* Alasan lembur

### 7.2 Persetujuan dan Perhitungan

* Persetujuan oleh atasan/HRD
* Perhitungan total jam lembur
* Riwayat lembur per karyawan

---

## 8. Notifikasi Sistem

Fitur untuk memberikan informasi kepada pengguna.

### 8.1 Jenis Notifikasi

* Presensi berhasil/gagal
* Pengajuan izin, cuti, dan lembur
* Status persetujuan

### 8.2 Media Notifikasi

* Notifikasi dalam sistem
* Email (opsional)
* Riwayat notifikasi

---

## 9. Audit Log dan Riwayat Aktivitas

Digunakan untuk keamanan dan transparansi sistem.

### 9.1 Aktivitas yang Dicatat

* Login dan logout
* Presensi
* Perubahan data

### 9.2 Informasi Log

* Pengguna
* Aktivitas
* Waktu
* IP address

### 9.3 Keamanan Log

* Log tidak dapat dihapus sembarangan
* Mendukung audit internal

---

## 10. Tech Stack yang Digunakan

Bagian ini menjelaskan teknologi yang digunakan dalam pengembangan sistem presensi karyawan berbasis website.

### 10.1 Bahasa Pemrograman

* **Python**

  * Digunakan sebagai bahasa pemrograman utama pada sisi backend
  * Menangani logika bisnis, autentikasi, presensi, pengolahan data, dan integrasi database
  * Dapat menggunakan framework seperti **Flask**

### 10.2 Arsitektur Sistem (MVC)

Sistem presensi karyawan ini menerapkan arsitektur **MVC (Model-View-Controller)** untuk memisahkan logika aplikasi, tampilan, dan pengelolaan data agar sistem lebih terstruktur dan mudah dikembangkan.

* **Model**

  * Mengelola data dan interaksi dengan database SQL Server
  * Berisi struktur tabel dan query (data karyawan, presensi, izin, cuti, lembur, audit log)

* **View**

  * Menampilkan antarmuka pengguna (UI)
  * Dibangun menggunakan HTML, CSS, dan JavaScript
  * Menyajikan halaman login, dashboard, presensi, dan laporan

* **Controller**

  * Menjembatani Model dan View
  * Mengelola alur logika aplikasi
  * Memproses input pengguna dan menentukan respons sistem

### 10.3 Database

* **Microsoft SQL Server**

  * Digunakan sebagai sistem manajemen basis data (DBMS)
  * Menyimpan data karyawan, presensi, izin, cuti, lembur, dan audit log
  * Mendukung relasi data, transaksi, dan keamanan data

### 10.4 Frontend Framework & UI

* **Flowbite**

  * Digunakan sebagai komponen antarmuka pengguna (UI)
  * Berbasis **Tailwind CSS**
  * Menyediakan komponen siap pakai seperti:

    * Form login dan input data
    * Tabel data karyawan dan presensi
    * Modal konfirmasi
    * Notifikasi dan alert
  * Mempercepat pengembangan tampilan yang responsif dan konsisten

---

## Penutup

Dokumen ini dapat digunakan sebagai dasar perancangan sistem presensi karyawan berbasis website, baik untuk keperluan akademik maupun implementasi di perusahaan.
