"""
Aplikasi Demo - Menjalankan aplikasi tanpa database
Hanya untuk melihat tampilan UI
"""
from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from config import Config
from utils.mock_data import (
    get_mock_attendances, get_mock_employees, get_mock_leave_requests,
    get_mock_overtimes, get_mock_notifications, get_mock_audit_logs,
    MockAttendance, MockEmployee, MockLeaveRequest, MockOvertime
)
from datetime import datetime, date

app = Flask(__name__)
app.config.from_object(Config)
app.config['DEMO_MODE'] = True

# Create blueprints
dashboard_bp = Blueprint('dashboard', __name__)
auth_bp = Blueprint('auth', __name__)
attendance_bp = Blueprint('attendance', __name__)
employee_bp = Blueprint('employee', __name__)
leave_bp = Blueprint('leave', __name__)
overtime_bp = Blueprint('overtime', __name__)
audit_bp = Blueprint('audit', __name__)
notification_bp = Blueprint('notification', __name__)

# Demo session untuk bypass login
@app.before_request
def setup_demo_session():
    """Setup demo session jika belum ada"""
    if 'user_id' not in session:
        # Set demo session (bisa ganti role di sini: admin, hrd, atasan, karyawan)
        session['user_id'] = 1
        session['username'] = 'demo_user'
        session['role'] = request.args.get('role', 'karyawan')  # Bisa ganti via ?role=admin
        session['employee_id'] = 1
        session.permanent = True

# ==================== ROUTES ====================

@dashboard_bp.route('/')
def index():
    """Dashboard dengan mock data"""
    role = session.get('role', 'karyawan')
    stats = {}
    notifications = get_mock_notifications(5)
    
    if role == 'karyawan':
        today_attendance = MockAttendance(
            attendance_date=date.today(),
            check_in_time=datetime.now().replace(hour=7, minute=30),
            status='hadir'
        )
        stats['today_attendance'] = today_attendance
        stats['pending_leaves'] = 2
        stats['pending_overtimes'] = 1
    elif role in ['admin', 'hrd']:
        stats['total_employees'] = 10
        stats['today_attendances'] = 8
        stats['pending_leaves'] = 5
        stats['pending_overtimes'] = 3
    elif role == 'atasan':
        stats['subordinates'] = 5
        stats['pending_leaves'] = 3
        stats['pending_overtimes'] = 2
    
    return render_template('dashboard/index.html', stats=stats, notifications=notifications, role=role)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Demo login - langsung redirect ke dashboard"""
    if request.method == 'POST':
        # Demo: langsung set session dan redirect
        role = request.form.get('role', 'karyawan')
        session['user_id'] = 1
        session['username'] = request.form.get('username', 'demo_user')
        session['role'] = role
        session['employee_id'] = 1
        session.permanent = True
        flash('Login berhasil (Demo Mode)', 'success')
        return redirect(url_for('dashboard.index'))
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Demo logout"""
    session.clear()
    flash('Anda telah logout', 'info')
    return redirect(url_for('auth.login'))

@attendance_bp.route('/')
def index():
    """Halaman presensi dengan mock data"""
    role = session.get('role', 'karyawan')
    today_attendance = MockAttendance(
        attendance_date=date.today(),
        check_in_time=datetime.now().replace(hour=7, minute=30),
        status='hadir'
    )
    attendances = get_mock_attendances(10)
    return render_template('attendance/index.html', 
                         today_attendance=today_attendance,
                         attendances=attendances,
                         role=role)

@attendance_bp.route('/check-in', methods=['POST'])
def check_in():
    """Demo check-in"""
    return jsonify({
        'success': True,
        'message': 'Check-in berhasil (Demo Mode)',
        'check_in_time': datetime.now().isoformat(),
        'status': 'hadir'
    })

@attendance_bp.route('/check-out', methods=['POST'])
def check_out():
    """Demo check-out"""
    return jsonify({
        'success': True,
        'message': 'Check-out berhasil (Demo Mode)',
        'check_out_time': datetime.now().isoformat()
    })

@attendance_bp.route('/history')
def history():
    """Riwayat presensi dengan mock data"""
    role = session.get('role', 'karyawan')
    attendances = get_mock_attendances(20)
    return render_template('attendance/history.html', attendances=attendances, role=role)

@employee_bp.route('/')
def index():
    """Daftar karyawan dengan mock data"""
    employees = get_mock_employees(10)
    return render_template('employee/index.html', employees=employees)

@employee_bp.route('/create', methods=['GET', 'POST'])
def create():
    """Tambah karyawan (demo)"""
    if request.method == 'POST':
        flash('Karyawan berhasil ditambahkan (Demo Mode)', 'success')
        return redirect(url_for('employee.index'))
    supervisors = get_mock_employees(5)
    return render_template('employee/create.html', supervisors=supervisors)

@employee_bp.route('/<int:employee_id>/edit', methods=['GET', 'POST'])
def edit(employee_id):
    """Edit karyawan (demo)"""
    if request.method == 'POST':
        flash('Data karyawan berhasil diupdate (Demo Mode)', 'success')
        return redirect(url_for('employee.index'))
    employee = MockEmployee(id=employee_id, full_name='John Doe')
    supervisors = get_mock_employees(5)
    return render_template('employee/edit.html', employee=employee, supervisors=supervisors)

@employee_bp.route('/<int:employee_id>/delete', methods=['POST'])
def delete(employee_id):
    """Hapus karyawan (demo)"""
    flash('Karyawan berhasil dinonaktifkan (Demo Mode)', 'success')
    return redirect(url_for('employee.index'))

@employee_bp.route('/import', methods=['GET', 'POST'])
def import_data():
    """Import karyawan (demo)"""
    if request.method == 'POST':
        flash('Berhasil mengimport data karyawan (Demo Mode)', 'success')
        return redirect(url_for('employee.index'))
    return render_template('employee/import.html')

@employee_bp.route('/export')
def export_data():
    """Export karyawan (demo)"""
    flash('Export berhasil (Demo Mode)', 'success')
    return redirect(url_for('employee.index'))

@leave_bp.route('/')
def index():
    """Daftar pengajuan izin/cuti/sakit dengan mock data"""
    role = session.get('role', 'karyawan')
    leave_requests = get_mock_leave_requests(10)
    return render_template('leave/index.html', leave_requests=leave_requests, role=role)

@leave_bp.route('/create', methods=['GET', 'POST'])
def create():
    """Buat pengajuan izin/cuti/sakit (demo)"""
    if request.method == 'POST':
        flash('Pengajuan berhasil dikirim (Demo Mode)', 'success')
        return redirect(url_for('leave.index'))
    return render_template('leave/create.html')

@leave_bp.route('/<int:leave_id>/approve', methods=['POST'])
def approve(leave_id):
    """Approve pengajuan (demo)"""
    flash('Pengajuan berhasil disetujui (Demo Mode)', 'success')
    return redirect(url_for('leave.index'))

@leave_bp.route('/<int:leave_id>/reject', methods=['POST'])
def reject(leave_id):
    """Reject pengajuan (demo)"""
    flash('Pengajuan ditolak (Demo Mode)', 'info')
    return redirect(url_for('leave.index'))

@overtime_bp.route('/')
def index():
    """Daftar pengajuan lembur dengan mock data"""
    role = session.get('role', 'karyawan')
    overtimes = get_mock_overtimes(10)
    return render_template('overtime/index.html', overtimes=overtimes, role=role)

@overtime_bp.route('/create', methods=['GET', 'POST'])
def create():
    """Buat pengajuan lembur (demo)"""
    if request.method == 'POST':
        flash('Pengajuan lembur berhasil dikirim (Demo Mode)', 'success')
        return redirect(url_for('overtime.index'))
    return render_template('overtime/create.html')

@overtime_bp.route('/<int:overtime_id>/approve', methods=['POST'])
def approve(overtime_id):
    """Approve lembur (demo)"""
    flash('Pengajuan lembur berhasil disetujui (Demo Mode)', 'success')
    return redirect(url_for('overtime.index'))

@overtime_bp.route('/<int:overtime_id>/reject', methods=['POST'])
def reject(overtime_id):
    """Reject lembur (demo)"""
    flash('Pengajuan lembur ditolak (Demo Mode)', 'info')
    return redirect(url_for('overtime.index'))

@audit_bp.route('/')
def index():
    """Audit log dengan mock data"""
    logs = get_mock_audit_logs(50)
    return render_template('audit/index.html', logs=logs)

@notification_bp.route('/')
def index():
    """Notifikasi dengan mock data"""
    notifications = get_mock_notifications(10)
    return jsonify([{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'notification_type': n.notification_type,
        'is_read': n.is_read,
        'created_at': n.created_at.isoformat()
    } for n in notifications])

@notification_bp.route('/unread')
def unread():
    """Notifikasi belum dibaca"""
    notifications = [n for n in get_mock_notifications(10) if not n.is_read]
    return jsonify([{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'notification_type': n.notification_type,
        'is_read': n.is_read,
        'created_at': n.created_at.isoformat()
    } for n in notifications])

@notification_bp.route('/<int:notification_id>/read', methods=['POST'])
def mark_read(notification_id):
    """Mark notifikasi as read (demo)"""
    return jsonify({'success': True})

@app.route('/change-role')
def change_role():
    """Ubah role untuk demo (untuk testing tampilan berbeda)"""
    role = request.args.get('role', 'karyawan')
    session['role'] = role
    flash(f'Role diubah menjadi: {role.upper()}', 'info')
    return redirect(url_for('dashboard.index'))

# Register blueprints SETELAH semua route didefinisikan
app.register_blueprint(dashboard_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(attendance_bp, url_prefix='/attendance')
app.register_blueprint(employee_bp, url_prefix='/employee')
app.register_blueprint(leave_bp, url_prefix='/leave')
app.register_blueprint(overtime_bp, url_prefix='/overtime')
app.register_blueprint(audit_bp, url_prefix='/audit')
app.register_blueprint(notification_bp, url_prefix='/notification')

if __name__ == '__main__':
    print("="*60)
    print("🚀 DEMO MODE - Aplikasi berjalan tanpa database")
    print("="*60)
    print("\n📝 Catatan:")
    print("  - Semua data adalah MOCK DATA (tidak tersimpan)")
    print("  - Tidak memerlukan koneksi database")
    print("  - Hanya untuk melihat tampilan UI")
    print("\n🔑 Login:")
    print("  - Username: (bebas)")
    print("  - Password: (bebas)")
    print("  - Atau langsung akses: http://localhost:5000")
    print("\n👤 Ganti Role untuk melihat tampilan berbeda:")
    print("  - http://localhost:5000/change-role?role=karyawan")
    print("  - http://localhost:5000/change-role?role=atasan")
    print("  - http://localhost:5000/change-role?role=hrd")
    print("  - http://localhost:5000/change-role?role=admin")
    print("\n🌐 Aplikasi berjalan di: http://localhost:5000")
    print("="*60)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
