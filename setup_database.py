"""
Script Python untuk setup database SQL Server secara otomatis
Membuat database jika belum ada, kemudian menjalankan init_db.py
"""
import pyodbc
import sys
import os

# Konfigurasi koneksi SQL Server
SERVER = os.environ.get('SQL_SERVER', 'localhost')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'AbsensiDB')
SQL_USERNAME = os.environ.get('SQL_USERNAME', 'sa')
SQL_PASSWORD = os.environ.get('SQL_PASSWORD', '')
USE_WINDOWS_AUTH = os.environ.get('USE_WINDOWS_AUTH', 'true').lower() in ['true', '1', 'yes']

def create_database():
    """Membuat database jika belum ada"""
    try:
        # Koneksi ke master database untuk membuat database baru
        if USE_WINDOWS_AUTH:
            conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE=master;Trusted_Connection=yes;'
        else:
            conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE=master;UID={SQL_USERNAME};PWD={SQL_PASSWORD};'
        
        print(f"Mencoba koneksi ke SQL Server: {SERVER}...")
        conn = pyodbc.connect(conn_str, timeout=5)
        cursor = conn.cursor()
        
        # Cek apakah database sudah ada
        cursor.execute(f"SELECT name FROM sys.databases WHERE name = '{DATABASE_NAME}'")
        if cursor.fetchone():
            print(f"✓ Database '{DATABASE_NAME}' sudah ada.")
        else:
            # Buat database baru
            print(f"Membuat database '{DATABASE_NAME}'...")
            cursor.execute(f"CREATE DATABASE [{DATABASE_NAME}]")
            conn.commit()
            print(f"✓ Database '{DATABASE_NAME}' berhasil dibuat.")
        
        cursor.close()
        conn.close()
        return True
        
    except pyodbc.Error as e:
        print(f"❌ Error saat membuat database: {e}")
        print("\nTroubleshooting:")
        print("1. Pastikan SQL Server sudah berjalan")
        print("2. Pastikan ODBC Driver 17 for SQL Server sudah terinstall")
        print("3. Cek koneksi dengan mengubah SERVER, SQL_USERNAME, SQL_PASSWORD di script ini")
        print("4. Atau buat database manual dengan menjalankan setup_database.sql")
        return False
    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
        return False

def main():
    """Main function"""
    print("="*60)
    print("Setup Database Sistem Presensi Karyawan")
    print("="*60)
    print()
    
    # Buat database
    if not create_database():
        print("\n❌ Gagal membuat database. Silakan cek error di atas.")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("Database berhasil dibuat!")
    print("="*60)
    print("\nSelanjutnya:")
    print("1. Pastikan config.py sudah dikonfigurasi dengan benar")
    print("2. Jalankan: python init_db.py")
    print("3. Jalankan: python app.py")
    print("="*60)

if __name__ == '__main__':
    main()
