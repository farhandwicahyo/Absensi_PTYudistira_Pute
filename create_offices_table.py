"""
Script untuk membuat tabel offices di database
Jalankan script ini jika tabel offices belum ada
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import create_app
from models import db
from models.office import Office

app = create_app()

with app.app_context():
    print("="*60)
    print("Membuat tabel offices...")
    print("="*60)
    
    try:
        # Create all tables (termasuk offices jika belum ada)
        db.create_all()
        print("[OK] Tabel offices berhasil dibuat/diverifikasi")
        
        # Cek apakah tabel sudah ada
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'offices' in tables:
            print("[OK] Tabel 'offices' sudah ada di database")
            
            # Hitung jumlah kantor
            count = Office.query.count()
            print(f"[INFO] Jumlah lokasi kantor saat ini: {count}")
        else:
            print("[WARNING] Tabel 'offices' tidak ditemukan di database")
            print("[INFO] Silakan cek koneksi database dan pastikan model Office sudah di-import")
        
    except Exception as e:
        print(f"[ERROR] Gagal membuat tabel: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("="*60)
