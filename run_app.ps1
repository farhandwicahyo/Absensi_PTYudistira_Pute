# Script untuk menjalankan aplikasi Sistem Presensi Karyawan
# Pastikan SQL Server sudah berjalan dan database AbsensiDB sudah dibuat

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Sistem Presensi Karyawan" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set environment variables untuk database
$env:USE_WINDOWS_AUTH = "true"
$env:SQL_SERVER = "localhost"
$env:DATABASE_NAME = "AbsensiDB"
$env:DEMO_MODE = "false"

Write-Host "Konfigurasi Database:" -ForegroundColor Yellow
Write-Host "  - Server: $env:SQL_SERVER" -ForegroundColor Gray
Write-Host "  - Database: $env:DATABASE_NAME" -ForegroundColor Gray
Write-Host "  - Authentication: Windows Authentication" -ForegroundColor Gray
Write-Host ""

# Cek apakah database ada
Write-Host "Memeriksa database..." -ForegroundColor Yellow
$dbCheck = sqlcmd -S localhost -Q "SELECT name FROM sys.databases WHERE name = 'AbsensiDB'" -E -h -1 2>$null
if ($LASTEXITCODE -ne 0 -or -not $dbCheck) {
    Write-Host "[ERROR] Database AbsensiDB tidak ditemukan!" -ForegroundColor Red
    Write-Host "Jalankan script berikut untuk membuat database:" -ForegroundColor Yellow
    Write-Host "  sqlcmd -S localhost -Q \"CREATE DATABASE AbsensiDB\" -E" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Atau jalankan: python init_db.py" -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] Database AbsensiDB ditemukan" -ForegroundColor Green
Write-Host ""

# Jalankan aplikasi
Write-Host "Menjalankan aplikasi..." -ForegroundColor Yellow
Write-Host "Aplikasi akan berjalan di: http://localhost:5000 (localhost saja)" -ForegroundColor Cyan
Write-Host "Aplikasi hanya dapat diakses dari komputer ini, tidak dari jaringan lain" -ForegroundColor Gray
Write-Host ""
Write-Host "Default Login:" -ForegroundColor Yellow
Write-Host "  Admin: username='admin', password='admin123'" -ForegroundColor Gray
Write-Host "  HRD:   username='hrd',   password='hrd123'" -ForegroundColor Gray
Write-Host ""
Write-Host "Tekan Ctrl+C untuk menghentikan aplikasi" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

python app.py
