"""
Script untuk membuat user account untuk karyawan yang sudah ada
"""
import os
from dotenv import load_dotenv

# Load environment variables dari .env file
load_dotenv()

from app import create_app
from models import db
from models.user import User
from models.employee import Employee

app = create_app()

with app.app_context():
    # Cari karyawan berdasarkan NIK atau ID
    employee = Employee.query.filter_by(nik='LJICE25004').first()
    
    if not employee:
        print("[ERROR] Karyawan dengan NIK 'LJICE25004' tidak ditemukan!")
        print("Mencari berdasarkan ID 3...")
        employee = Employee.query.get(3)
    
    if not employee:
        print("[ERROR] Karyawan dengan ID 3 tidak ditemukan!")
        exit(1)
    
    print(f"[OK] Karyawan ditemukan: {employee.full_name} (NIK: {employee.nik})")
    
    # Cek apakah user sudah ada
    existing_user = User.query.filter_by(employee_id=employee.id).first()
    if existing_user:
        print(f"[WARNING] User account sudah ada untuk karyawan ini!")
        print(f"   Username: {existing_user.username}")
        print(f"   Email: {existing_user.email}")
        print(f"   Role: {existing_user.role}")
        response = input("\nApakah Anda ingin membuat user baru? (y/n): ")
        if response.lower() != 'y':
            print("Dibatalkan.")
            exit(0)
    
    # Cek apakah username atau email sudah digunakan
    username = employee.nik.lower()
    email = employee.email.lower()
    
    if User.query.filter_by(username=username).first():
        print(f"[WARNING] Username '{username}' sudah digunakan!")
        username = input("Masukkan username baru: ").strip()
        if not username:
            print("[ERROR] Username tidak boleh kosong!")
            exit(1)
    
    if User.query.filter_by(email=email).first():
        print(f"[WARNING] Email '{email}' sudah digunakan!")
        email = input("Masukkan email baru: ").strip()
        if not email:
            print("[ERROR] Email tidak boleh kosong!")
            exit(1)
    
    # Tentukan role
    print("\nPilih role untuk user:")
    print("1. Karyawan (default)")
    print("2. Atasan")
    print("3. HRD")
    print("4. Admin")
    role_choice = input("Pilihan (1-4, default: 1): ").strip() or "1"
    
    role_map = {
        "1": "karyawan",
        "2": "atasan",
        "3": "hrd",
        "4": "admin"
    }
    user_role = role_map.get(role_choice, "karyawan")
    
    # Password
    password = input(f"\nMasukkan password (default: {employee.nik}): ").strip() or employee.nik
    
    # Buat user
    user = User(
        username=username,
        email=email,
        role=user_role,
        employee_id=employee.id,
        is_active=True
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    print("\n" + "="*50)
    print("[SUCCESS] User account berhasil dibuat!")
    print("="*50)
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"Role: {user_role}")
    print(f"Employee: {employee.full_name} (NIK: {employee.nik})")
    print("="*50)
    print("\n[WARNING] PENTING: Simpan informasi login ini dengan aman!")
    print("   Disarankan untuk mengubah password setelah login pertama kali.")
