# Script untuk setup database Sistem Presensi Karyawan

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Database - Sistem Presensi Karyawan" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set environment variables
$env:USE_WINDOWS_AUTH = "true"
$env:SQL_SERVER = "localhost"
$env:DATABASE_NAME = "AbsensiDB"
$env:DEMO_MODE = "false"

# Cek apakah database sudah ada
Write-Host "Memeriksa database AbsensiDB..." -ForegroundColor Yellow
$dbExists = sqlcmd -S localhost -Q "SELECT name FROM sys.databases WHERE name = 'AbsensiDB'" -E -h -1 2>$null

if ($LASTEXITCODE -eq 0 -and $dbExists) {
    Write-Host "[OK] Database AbsensiDB sudah ada" -ForegroundColor Green
    $createDb = Read-Host "Apakah Anda ingin membuat ulang database? (y/n)"
    if ($createDb -eq 'y' -or $createDb -eq 'Y') {
        Write-Host "Menghapus database lama..." -ForegroundColor Yellow
        sqlcmd -S localhost -Q "DROP DATABASE AbsensiDB" -E 2>$null
        Write-Host "Membuat database baru..." -ForegroundColor Yellow
        sqlcmd -S localhost -Q "CREATE DATABASE AbsensiDB" -E
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Database berhasil dibuat" -ForegroundColor Green
        } else {
            Write-Host "[ERROR] Gagal membuat database" -ForegroundColor Red
            exit 1
        }
    }
} else {
    Write-Host "Membuat database AbsensiDB..." -ForegroundColor Yellow
    sqlcmd -S localhost -Q "CREATE DATABASE AbsensiDB" -E
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Database berhasil dibuat" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Gagal membuat database. Pastikan SQL Server berjalan." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Menginisialisasi tabel dan user default..." -ForegroundColor Yellow
python init_db.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Setup database selesai!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Default users:" -ForegroundColor Yellow
    Write-Host "  Admin: username='admin', password='admin123'" -ForegroundColor Gray
    Write-Host "  HRD:   username='hrd',   password='hrd123'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Jalankan aplikasi dengan: .\run_app.ps1" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "[ERROR] Gagal menginisialisasi database" -ForegroundColor Red
    exit 1
}
