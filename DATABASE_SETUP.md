# Panduan Setup Database

## Konfigurasi Database

File ini menjelaskan cara mengkonfigurasi database untuk aplikasi.

### Opsi 1: Windows Authentication (Recommended)

Set environment variable berikut di PowerShell:
```powershell
$env:USE_WINDOWS_AUTH="true"
$env:SQL_SERVER="localhost"
$env:DATABASE_NAME="AbsensiDB"
```

### Opsi 2: SQL Server Authentication

Set environment variable berikut di PowerShell:
```powershell
$env:USE_WINDOWS_AUTH="false"
$env:SQL_SERVER="localhost"
$env:DATABASE_NAME="AbsensiDB"
$env:SQL_USERNAME="sa"
$env:SQL_PASSWORD="YourPassword123"
```

### Membuat Database

Jalankan script SQL berikut di SQL Server Management Studio atau menggunakan sqlcmd:
```sql
CREATE DATABASE AbsensiDB;
```

Atau gunakan file `create_database.sql` yang sudah disediakan.

### Inisialisasi Database

Setelah database dibuat, jalankan:
```bash
python init_db.py
```

Script ini akan:
- Membuat semua tabel yang diperlukan
- Membuat user default (admin dan hrd)

### Default Users

Setelah inisialisasi, gunakan kredensial berikut:
- **Admin**: username=`admin`, password=`admin123`
- **HRD**: username=`hrd`, password=`hrd123`

⚠️ **PENTING**: Ganti password default setelah login pertama kali!
