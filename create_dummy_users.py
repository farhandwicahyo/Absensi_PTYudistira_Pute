"""
Script untuk menambahkan akun dummy: 2 atasan dan 5 karyawan
"""
import os
from dotenv import load_dotenv

# Load environment variables dari .env file
load_dotenv()

from app import create_app
from models import db
from models.user import User
from models.employee import Employee
from datetime import date

app = create_app()

with app.app_context():
    print("="*60)
    print("Menambahkan Akun Dummy: 2 Atasan dan 5 Karyawan")
    print("="*60)
    
    # Data untuk 2 atasan
    supervisors_data = [
        {
            'nik': 'ATASAN001',
            'full_name': 'Budi Santoso',
            'email': 'budi.santoso@company.com',
            'phone': '081234567001',
            'position': 'Manager IT',
            'division': 'IT',
            'username': 'atasan1',
            'password': 'atasan123'
        },
        {
            'nik': 'ATASAN002',
            'full_name': 'Siti Nurhaliza',
            'email': 'siti.nurhaliza@company.com',
            'phone': '081234567002',
            'position': 'Manager HRD',
            'division': 'HRD',
            'username': 'atasan2',
            'password': 'atasan123'
        }
    ]
    
    # Data untuk 5 karyawan
    employees_data = [
        {
            'nik': 'KARYAWAN001',
            'full_name': 'Ahmad Fauzi',
            'email': 'ahmad.fauzi@company.com',
            'phone': '081234567101',
            'position': 'Software Developer',
            'division': 'IT',
            'username': 'karyawan1',
            'password': 'karyawan123',
            'supervisor_nik': 'ATASAN001'  # Dibawah atasan pertama
        },
        {
            'nik': 'KARYAWAN002',
            'full_name': 'Dewi Sartika',
            'email': 'dewi.sartika@company.com',
            'phone': '081234567102',
            'position': 'Frontend Developer',
            'division': 'IT',
            'username': 'karyawan2',
            'password': 'karyawan123',
            'supervisor_nik': 'ATASAN001'  # Dibawah atasan pertama
        },
        {
            'nik': 'KARYAWAN003',
            'full_name': 'Rizki Pratama',
            'email': 'rizki.pratama@company.com',
            'phone': '081234567103',
            'position': 'Backend Developer',
            'division': 'IT',
            'username': 'karyawan3',
            'password': 'karyawan123',
            'supervisor_nik': 'ATASAN001'  # Dibawah atasan pertama
        },
        {
            'nik': 'KARYAWAN004',
            'full_name': 'Indah Permata',
            'email': 'indah.permata@company.com',
            'phone': '081234567104',
            'position': 'HRD Staff',
            'division': 'HRD',
            'username': 'karyawan4',
            'password': 'karyawan123',
            'supervisor_nik': 'ATASAN002'  # Dibawah atasan kedua
        },
        {
            'nik': 'KARYAWAN005',
            'full_name': 'Bambang Wijaya',
            'email': 'bambang.wijaya@company.com',
            'phone': '081234567105',
            'position': 'HRD Staff',
            'division': 'HRD',
            'username': 'karyawan5',
            'password': 'karyawan123',
            'supervisor_nik': 'ATASAN002'  # Dibawah atasan kedua
        }
    ]
    
    # Membuat 2 atasan
    supervisor_ids = {}
    print("\n[1/2] Membuat akun Atasan...")
    for i, sup_data in enumerate(supervisors_data, 1):
        # Cek apakah employee sudah ada
        employee = Employee.query.filter_by(nik=sup_data['nik']).first()
        if not employee:
            employee = Employee(
                nik=sup_data['nik'],
                full_name=sup_data['full_name'],
                email=sup_data['email'],
                phone=sup_data['phone'],
                position=sup_data['position'],
                division=sup_data['division'],
                status='aktif',
                hire_date=date.today()
            )
            db.session.add(employee)
            db.session.commit()
            print(f"  [OK] Employee atasan {i} dibuat: {sup_data['full_name']} ({sup_data['nik']})")
        else:
            print(f"  [SKIP] Employee atasan {i} sudah ada: {sup_data['full_name']} ({sup_data['nik']})")
        
        # Simpan ID untuk referensi supervisor
        supervisor_ids[sup_data['nik']] = employee.id
        
        # Cek apakah user sudah ada
        user = User.query.filter_by(username=sup_data['username']).first()
        if not user:
            user = User(
                username=sup_data['username'],
                email=sup_data['email'],
                role='atasan',
                employee_id=employee.id,
                is_active=True
            )
            user.set_password(sup_data['password'])
            db.session.add(user)
            db.session.commit()
            print(f"  [OK] User atasan {i} dibuat: username='{sup_data['username']}', password='{sup_data['password']}'")
        else:
            print(f"  [SKIP] User atasan {i} sudah ada: username='{sup_data['username']}'")
    
    # Membuat 5 karyawan
    print("\n[2/2] Membuat akun Karyawan...")
    for i, emp_data in enumerate(employees_data, 1):
        # Cek apakah employee sudah ada
        employee = Employee.query.filter_by(nik=emp_data['nik']).first()
        if not employee:
            # Dapatkan supervisor_id
            supervisor_id = supervisor_ids.get(emp_data['supervisor_nik'])
            
            employee = Employee(
                nik=emp_data['nik'],
                full_name=emp_data['full_name'],
                email=emp_data['email'],
                phone=emp_data['phone'],
                position=emp_data['position'],
                division=emp_data['division'],
                supervisor_id=supervisor_id,
                status='aktif',
                hire_date=date.today()
            )
            db.session.add(employee)
            db.session.commit()
            print(f"  [OK] Employee karyawan {i} dibuat: {emp_data['full_name']} ({emp_data['nik']})")
        else:
            print(f"  [SKIP] Employee karyawan {i} sudah ada: {emp_data['full_name']} ({emp_data['nik']})")
        
        # Cek apakah user sudah ada
        user = User.query.filter_by(username=emp_data['username']).first()
        if not user:
            user = User(
                username=emp_data['username'],
                email=emp_data['email'],
                role='karyawan',
                employee_id=employee.id,
                is_active=True
            )
            user.set_password(emp_data['password'])
            db.session.add(user)
            db.session.commit()
            print(f"  [OK] User karyawan {i} dibuat: username='{emp_data['username']}', password='{emp_data['password']}'")
        else:
            print(f"  [SKIP] User karyawan {i} sudah ada: username='{emp_data['username']}'")
    
    print("\n" + "="*60)
    print("Selesai! Akun dummy berhasil ditambahkan")
    print("="*60)
    print("\nDaftar Akun Atasan:")
    print("  1. username='atasan1', password='atasan123' (Budi Santoso - Manager IT)")
    print("  2. username='atasan2', password='atasan123' (Siti Nurhaliza - Manager HRD)")
    print("\nDaftar Akun Karyawan:")
    print("  1. username='karyawan1', password='karyawan123' (Ahmad Fauzi - Software Developer)")
    print("  2. username='karyawan2', password='karyawan123' (Dewi Sartika - Frontend Developer)")
    print("  3. username='karyawan3', password='karyawan123' (Rizki Pratama - Backend Developer)")
    print("  4. username='karyawan4', password='karyawan123' (Indah Permata - HRD Staff)")
    print("  5. username='karyawan5', password='karyawan123' (Bambang Wijaya - HRD Staff)")
    print("\n[WARNING] PENTING: Ganti password default setelah login pertama kali!")
    print("="*60)
