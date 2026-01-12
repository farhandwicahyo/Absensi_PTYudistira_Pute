-- Script untuk membuat database AbsensiDB
-- Jalankan script ini di SQL Server Management Studio atau menggunakan sqlcmd

-- Buat database jika belum ada
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

-- Gunakan database AbsensiDB
USE AbsensiDB;
GO

PRINT 'Database AbsensiDB siap digunakan.';
PRINT 'Selanjutnya jalankan: python init_db.py untuk membuat tabel dan user default.';
GO
