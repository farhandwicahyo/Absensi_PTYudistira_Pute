"""
Script setup lengkap untuk Sistem Presensi Karyawan
Menjalankan semua langkah setup secara otomatis
"""
import os
import sys
import subprocess

def print_header(text):
    """Print header dengan format"""
    print("\n" + "="*60)
    print(text)
    print("="*60)

def print_step(step_num, text):
    """Print step dengan format"""
    print(f"\n[{step_num}] {text}")
    print("-" * 60)

def check_python():
    """Cek versi Python"""
    print_step(1, "Mengecek Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ diperlukan!")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} terdeteksi")
    return True

def install_dependencies():
    """Install dependencies"""
    print_step(2, "Menginstall dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies berhasil diinstall")
        return True
    except subprocess.CalledProcessError:
        print("❌ Gagal menginstall dependencies")
        return False

def setup_database():
    """Setup database"""
    print_step(3, "Setup database...")
    print("Mencoba membuat database...")
    try:
        from setup_database import create_database
        if create_database():
            print("✓ Database berhasil dibuat/disiapkan")
            return True
        else:
            print("⚠️  Database mungkin sudah ada atau ada masalah koneksi")
            print("   Lanjutkan jika database sudah dibuat manual")
            response = input("   Lanjutkan setup? (y/n): ")
            return response.lower() == 'y'
    except Exception as e:
        print(f"⚠️  Error: {e}")
        print("   Anda bisa membuat database manual dengan menjalankan setup_database.sql")
        response = input("   Lanjutkan setup? (y/n): ")
        return response.lower() == 'y'

def init_database():
    """Inisialisasi database (membuat tabel dan user default)"""
    print_step(4, "Inisialisasi database (membuat tabel dan user default)...")
    try:
        subprocess.check_call([sys.executable, "init_db.py"])
        print("✓ Database berhasil diinisialisasi")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Gagal menginisialisasi database: {e}")
        print("\nTroubleshooting:")
        print("1. Pastikan SQL Server sudah berjalan")
        print("2. Pastikan database sudah dibuat")
        print("3. Cek konfigurasi di config.py atau environment variables")
        return False

def create_env_file():
    """Membuat file .env jika belum ada"""
    print_step(5, "Menyiapkan file konfigurasi...")
    if os.path.exists('.env'):
        print("✓ File .env sudah ada")
        return True
    
    print("File .env tidak ditemukan. Membuat file .env...")
    env_content = """# Konfigurasi Database SQL Server
SQL_SERVER=localhost
DATABASE_NAME=AbsensiDB
SQL_USERNAME=sa
SQL_PASSWORD=
USE_WINDOWS_AUTH=true

# Flask Secret Key
SECRET_KEY=dev-secret-key-change-in-production

# Demo Mode (false untuk menggunakan database real)
DEMO_MODE=false
"""
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✓ File .env berhasil dibuat")
        print("⚠️  Silakan edit file .env jika perlu mengubah konfigurasi")
        return True
    except Exception as e:
        print(f"⚠️  Tidak bisa membuat file .env: {e}")
        print("   Anda bisa membuat manual atau menggunakan environment variables")
        return True

def create_uploads_folder():
    """Membuat folder uploads jika belum ada"""
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        print("✓ Folder uploads berhasil dibuat")

def main():
    """Main function"""
    print_header("Setup Sistem Presensi Karyawan")
    print("\nScript ini akan:")
    print("1. Mengecek Python")
    print("2. Menginstall dependencies")
    print("3. Membuat database")
    print("4. Menginisialisasi database (tabel dan user default)")
    print("5. Menyiapkan file konfigurasi")
    
    input("\nTekan Enter untuk melanjutkan...")
    
    # Step 1: Check Python
    if not check_python():
        sys.exit(1)
    
    # Step 2: Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Step 3: Create .env file
    create_env_file()
    
    # Step 4: Create uploads folder
    create_uploads_folder()
    
    # Step 5: Setup database
    if not setup_database():
        print("\n❌ Setup database gagal. Silakan cek error di atas.")
        sys.exit(1)
    
    # Step 6: Initialize database
    if not init_database():
        print("\n❌ Inisialisasi database gagal. Silakan cek error di atas.")
        sys.exit(1)
    
    # Success
    print_header("Setup Selesai!")
    print("\n✓ Semua langkah setup berhasil!")
    print("\nDefault users:")
    print("  Admin: username='admin', password='admin123'")
    print("  HRD:   username='hrd',   password='hrd123'")
    print("\n⚠️  PENTING: Ganti password default setelah login pertama kali!")
    print("\nUntuk menjalankan aplikasi:")
    print("  python app.py")
    print("\nAplikasi akan berjalan di: http://localhost:5000")
    print("="*60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup dibatalkan oleh user.")
        sys.exit(1)
