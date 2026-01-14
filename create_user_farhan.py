"""
Script untuk membuat user account untuk karyawan FARHAN DWICAHYO
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
        print("[INFO] Mencari berdasarkan ID 3...")
        employee = Employee.query.get(3)
    
    if not employee:
        print("[ERROR] Karyawan tidak ditemukan!")
        print("Pastikan karyawan dengan NIK 'LJICE25004' atau ID 3 sudah ada di database.")
        exit(1)
    
    print(f"[OK] Karyawan ditemukan: {employee.full_name} (NIK: {employee.nik})")
    
    # Cek apakah user sudah ada
    existing_user = User.query.filter_by(employee_id=employee.id).first()
    if existing_user:
        print(f"[INFO] User account sudah ada untuk karyawan ini!")
        print(f"   Username: {existing_user.username}")
        print(f"   Email: {existing_user.email}")
        print(f"   Role: {existing_user.role}")
        print("\nUser account sudah dibuat sebelumnya.")
        exit(0)
    
    # Setup user data
    username = employee.nik.lower()  # ljice25004
    email = employee.email.lower()  # farhandwicahyo@pamapersada.net
    password = employee.nik  # Default password: NIK
    user_role = "karyawan"  # Default role
    
    # Cek apakah username atau email sudah digunakan
    if User.query.filter_by(username=username).first():
        print(f"[WARNING] Username '{username}' sudah digunakan!")
        username = f"{username}_1"  # Tambahkan suffix
        print(f"[INFO] Menggunakan username alternatif: {username}")
    
    if User.query.filter_by(email=email).first():
        print(f"[WARNING] Email '{email}' sudah digunakan!")
        print("[ERROR] Email sudah terdaftar sebagai user lain. Tidak bisa membuat user.")
        exit(1)
    
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
    
    print("\n" + "="*60)
    print("[SUCCESS] User account berhasil dibuat!")
    print("="*60)
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"Role: {user_role}")
    print(f"Employee: {employee.full_name} (NIK: {employee.nik})")
    print("="*60)
    print("\n[WARNING] PENTING: Simpan informasi login ini dengan aman!")
    print("   Disarankan untuk mengubah password setelah login pertama kali.")
    print("\nUntuk login, gunakan:")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
