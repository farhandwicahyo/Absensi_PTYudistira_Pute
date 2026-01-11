"""
Controller untuk manajemen data karyawan
"""
from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for, send_file
from models import db
from models.employee import Employee
from models.user import User
from utils.decorators import login_required, hrd_required
from utils.audit_logger import AuditLogger
from werkzeug.utils import secure_filename
import csv
import io
from datetime import datetime

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/')
@login_required
@hrd_required
def index():
    """Daftar karyawan"""
    employees = Employee.query.order_by(Employee.full_name).all()
    return render_template('employee/index.html', employees=employees)

@employee_bp.route('/create', methods=['GET', 'POST'])
@login_required
@hrd_required
def create():
    """Tambah karyawan baru"""
    if request.method == 'POST':
        nik = request.form.get('nik')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        position = request.form.get('position')
        division = request.form.get('division')
        supervisor_id = request.form.get('supervisor_id') or None
        hire_date = request.form.get('hire_date') or None
        
        # Validate
        if Employee.query.filter_by(nik=nik).first():
            flash('NIK sudah terdaftar', 'error')
            return render_template('employee/create.html')
        
        if Employee.query.filter_by(email=email).first():
            flash('Email sudah terdaftar', 'error')
            return render_template('employee/create.html')
        
        # Create employee
        employee = Employee(
            nik=nik,
            full_name=full_name,
            email=email,
            phone=phone,
            position=position,
            division=division,
            supervisor_id=int(supervisor_id) if supervisor_id else None,
            hire_date=datetime.strptime(hire_date, '%Y-%m-%d').date() if hire_date else None
        )
        
        db.session.add(employee)
        db.session.commit()
        
        # Log audit
        AuditLogger.log_data_change(
            session.get('user_id'),
            session.get('username'),
            'create',
            'employees',
            employee.id,
            f'Created employee: {full_name}'
        )
        
        flash('Karyawan berhasil ditambahkan', 'success')
        return redirect(url_for('employee.index'))
    
    # Get supervisors for dropdown
    supervisors = Employee.query.filter_by(status='aktif').all()
    return render_template('employee/create.html', supervisors=supervisors)

@employee_bp.route('/<int:employee_id>/edit', methods=['GET', 'POST'])
@login_required
@hrd_required
def edit(employee_id):
    """Edit data karyawan"""
    employee = Employee.query.get_or_404(employee_id)
    
    if request.method == 'POST':
        employee.nik = request.form.get('nik')
        employee.full_name = request.form.get('full_name')
        employee.email = request.form.get('email')
        employee.phone = request.form.get('phone')
        employee.position = request.form.get('position')
        employee.division = request.form.get('division')
        employee.supervisor_id = int(request.form.get('supervisor_id')) if request.form.get('supervisor_id') else None
        employee.status = request.form.get('status')
        
        if request.form.get('hire_date'):
            employee.hire_date = datetime.strptime(request.form.get('hire_date'), '%Y-%m-%d').date()
        
        db.session.commit()
        
        # Log audit
        AuditLogger.log_data_change(
            session.get('user_id'),
            session.get('username'),
            'update',
            'employees',
            employee.id,
            f'Updated employee: {employee.full_name}'
        )
        
        flash('Data karyawan berhasil diupdate', 'success')
        return redirect(url_for('employee.index'))
    
    supervisors = Employee.query.filter_by(status='aktif').all()
    return render_template('employee/edit.html', employee=employee, supervisors=supervisors)

@employee_bp.route('/<int:employee_id>/delete', methods=['POST'])
@login_required
@hrd_required
def delete(employee_id):
    """Hapus karyawan"""
    employee = Employee.query.get_or_404(employee_id)
    
    # Soft delete (ubah status)
    employee.status = 'nonaktif'
    db.session.commit()
    
    # Log audit
    AuditLogger.log_data_change(
        session.get('user_id'),
        session.get('username'),
        'delete',
        'employees',
        employee.id,
        f'Deleted employee: {employee.full_name}'
    )
    
    flash('Karyawan berhasil dinonaktifkan', 'success')
    return redirect(url_for('employee.index'))

@employee_bp.route('/import', methods=['GET', 'POST'])
@login_required
@hrd_required
def import_data():
    """Import data karyawan dari CSV/Excel"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('File tidak ditemukan', 'error')
            return redirect(url_for('employee.import_data'))
        
        file = request.files['file']
        if file.filename == '':
            flash('File tidak dipilih', 'error')
            return redirect(url_for('employee.import_data'))
        
        # Read CSV
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        
        imported = 0
        errors = []
        
        for row in csv_input:
            try:
                # Check if exists
                if Employee.query.filter_by(nik=row['nik']).first():
                    errors.append(f"NIK {row['nik']} sudah terdaftar")
                    continue
                
                employee = Employee(
                    nik=row['nik'],
                    full_name=row['full_name'],
                    email=row['email'],
                    phone=row.get('phone'),
                    position=row['position'],
                    division=row['division'],
                    status=row.get('status', 'aktif')
                )
                db.session.add(employee)
                imported += 1
            except Exception as e:
                errors.append(f"Error importing {row.get('nik', 'unknown')}: {str(e)}")
        
        db.session.commit()
        
        flash(f'Berhasil mengimport {imported} data karyawan', 'success')
        if errors:
            flash(f'Terjadi {len(errors)} error: {", ".join(errors[:5])}', 'warning')
        
        return redirect(url_for('employee.index'))
    
    return render_template('employee/import.html')

@employee_bp.route('/export')
@login_required
@hrd_required
def export_data():
    """Export data karyawan ke CSV"""
    employees = Employee.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['NIK', 'Nama Lengkap', 'Email', 'Phone', 'Jabatan', 'Divisi', 'Status'])
    
    # Data
    for emp in employees:
        writer.writerow([
            emp.nik,
            emp.full_name,
            emp.email,
            emp.phone or '',
            emp.position,
            emp.division,
            emp.status
        ])
    
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'employees_{datetime.now().strftime("%Y%m%d")}.csv'
    )
