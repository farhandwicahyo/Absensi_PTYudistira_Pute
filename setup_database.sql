-- Script SQL untuk membuat database Sistem Presensi Karyawan
-- Jalankan script ini di SQL Server Management Studio atau sqlcmd

-- Membuat database jika belum ada
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'AbsensiDB')
BEGIN
    CREATE DATABASE AbsensiDB;
    PRINT 'Database AbsensiDB berhasil dibuat.';
END
ELSE
BEGIN
    PRINT 'Database AbsensiDB sudah ada.';
END
GO

-- Menggunakan database yang baru dibuat
USE AbsensiDB;
GO

-- Catatan: Tabel akan dibuat otomatis oleh Flask-SQLAlchemy saat menjalankan init_db.py
-- Script ini hanya membuat database saja

PRINT 'Setup database selesai.';
PRINT 'Selanjutnya jalankan: python init_db.py untuk membuat tabel dan user default.';
GO
