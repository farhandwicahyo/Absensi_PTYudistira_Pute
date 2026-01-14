"""
Controller untuk pengajuan izin, cuti, dan sakit
"""
from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from models import db
from models.leave_request import LeaveRequest
from models.employee import Employee
from models.user import User
from utils.decorators import login_required, supervisor_required
from utils.audit_logger import AuditLogger
from utils.notification_helper import NotificationHelper
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from config import Config

leave_bp = Blueprint('leave', __name__)

@leave_bp.route('/')
@login_required
def index():
    """Daftar pengajuan Timeoff"""
    role = session.get('role')
    employee_id = session.get('employee_id')
    
    query = LeaveRequest.query
    
    if role == 'karyawan':
        query = query.filter_by(employee_id=employee_id)
    elif role == 'atasan':
        # Show subordinates' requests
        employee = Employee.query.get(employee_id)
        if employee:
            subordinate_ids = [e.id for e in employee.subordinates]
            query = query.filter(LeaveRequest.employee_id.in_(subordinate_ids))
    
    leave_requests = query.order_by(LeaveRequest.created_at.desc()).all()
    
    # Add approval status info for each request
    for leave in leave_requests:
        # Determine current approval stage
        if leave.status == 'ditolak':
            leave.approval_stage = 'ditolak'
        elif leave.status == 'disetujui':
            leave.approval_stage = 'disetujui'
        elif leave.leave_type == 'cuti':
            if not leave.supervisor_approval:
                leave.approval_stage = 'menunggu_atasan'
            elif not leave.hrd_approval:
                leave.approval_stage = 'menunggu_hrd'
            else:
                leave.approval_stage = 'disetujui'
        else:
            # Izin dan sakit
            if leave.supervisor_id and not leave.supervisor_approval:
                leave.approval_stage = 'menunggu_atasan'
            elif leave.supervisor_approval:
                leave.approval_stage = 'disetujui'
            else:
                leave.approval_stage = 'menunggu_approval'
    
    return render_template('leave/index.html', leave_requests=leave_requests, role=role)

@leave_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Buat pengajuan Timeoff"""
    employee_id = session.get('employee_id')
    
    if request.method == 'POST':
        leave_type = request.form.get('leave_type')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        reason = request.form.get('reason')
        
        # Get employee to find supervisor
        employee = Employee.query.get(employee_id)
        if not employee:
            flash('Data karyawan tidak ditemukan', 'error')
            return redirect(url_for('leave.index'))
        
        # Handle file upload
        attachment_path = None
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename:
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
                filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                file.save(filepath)
                attachment_path = filepath
        
        # Create leave request
        leave_request = LeaveRequest(
            employee_id=employee_id,
            leave_type=leave_type,
            start_date=datetime.strptime(start_date, '%Y-%m-%d').date(),
            end_date=datetime.strptime(end_date, '%Y-%m-%d').date(),
            reason=reason,
            attachment_path=attachment_path,
            supervisor_id=employee.supervisor_id
        )
        
        db.session.add(leave_request)
        db.session.commit()
        
        # Log audit
        AuditLogger.log_data_change(
            session.get('user_id'),
            session.get('username'),
            'create',
            'leave_requests',
            leave_request.id,
            f'Created {leave_type} request'
        )
        
        # Create notification for employee
        NotificationHelper.notify_leave_submitted(
            session.get('user_id'),
            leave_request.id,
            leave_type
        )
        
        # Create notification for supervisor if exists
        if employee.supervisor_id:
            supervisor_user = User.query.filter_by(employee_id=employee.supervisor_id).first()
            if supervisor_user:
                NotificationHelper.notify_supervisor_new_leave(
                    supervisor_user.id,
                    leave_request.id,
                    leave_type,
                    employee.full_name
                )
        
        flash('Pengajuan berhasil dikirim', 'success')
        return redirect(url_for('leave.index'))
    
    return render_template('leave/create.html')

@leave_bp.route('/<int:leave_id>/approve', methods=['POST'])
@login_required
@supervisor_required
def approve(leave_id):
    """Approve pengajuan"""
    leave_request = LeaveRequest.query.get_or_404(leave_id)
    role = session.get('role')
    user_id = session.get('user_id')
    
    # Check if can approve
    if role == 'atasan':
        if leave_request.supervisor_id != session.get('employee_id'):
            flash('Anda tidak berhak menyetujui pengajuan ini', 'error')
            return redirect(url_for('leave.index'))
        
        # Atasan approve
        leave_request.supervisor_approval = True
        leave_request.supervisor_approval_date = datetime.utcnow()
        
        # Untuk cuti, perlu approval HRD juga setelah atasan approve
        # Untuk izin/sakit, bisa langsung disetujui jika atasan sudah approve
        if leave_request.leave_type == 'cuti':
            # Cuti perlu approval HRD setelah atasan
            leave_request.status = 'menunggu_hrd'  # Status baru: menunggu HRD
        else:
            # Izin dan sakit bisa langsung disetujui setelah atasan approve
            if leave_request.hrd_approval:
                leave_request.status = 'disetujui'
            else:
                # Jika tidak perlu HRD approval, langsung disetujui
                leave_request.status = 'disetujui'
    
    elif role in ['admin', 'hrd']:
        # HRD/Admin bisa approve jika:
        # 1. Atasan sudah approve (untuk cuti wajib)
        # 2. Atau langsung approve jika tidak ada atasan
        if leave_request.leave_type == 'cuti' and leave_request.supervisor_id:
            # Untuk cuti, harus menunggu approval atasan dulu
            if not leave_request.supervisor_approval:
                flash('Pengajuan cuti harus disetujui oleh atasan terlebih dahulu', 'warning')
                return redirect(url_for('leave.index'))
        
        leave_request.hrd_approval = True
        leave_request.hrd_approval_date = datetime.utcnow()
        leave_request.hrd_id = user_id
        
        # Set status menjadi disetujui
        leave_request.status = 'disetujui'
    
    db.session.commit()
    
    # Log audit
    AuditLogger.log_data_change(
        user_id,
        session.get('username'),
        'approve',
        'leave_requests',
        leave_request.id,
        f'Approved {leave_request.leave_type} request'
    )
    
    # Create notification for employee
    employee_user = User.query.filter_by(employee_id=leave_request.employee_id).first()
    if employee_user:
        # Jika sudah final approval (disetujui), kirim notifikasi ke karyawan
        if leave_request.status == 'disetujui':
            NotificationHelper.notify_leave_approval(
                employee_user.id,
                leave_request.id,
                True,
                leave_request.leave_type,
                role
            )
        # Jika atasan approve tapi masih menunggu HRD (untuk cuti), kirim notifikasi intermediate
        elif leave_request.status == 'menunggu_hrd' and role == 'atasan':
            NotificationHelper.create_notification(
                employee_user.id,
                f'Pengajuan {leave_request.leave_type.capitalize()} Disetujui Atasan',
                f'Pengajuan {leave_request.leave_type} Anda telah disetujui atasan dan sedang menunggu approval HRD.',
                'leave',
                leave_request.id
            )
    
    # Jika atasan approve cuti, notifikasi ke HRD
    if role == 'atasan' and leave_request.leave_type == 'cuti' and leave_request.status == 'menunggu_hrd':
        # Notifikasi ke HRD bahwa ada pengajuan cuti yang sudah di-approve atasan
        hrd_users = User.query.filter(User.role.in_(['hrd', 'admin'])).all()
        for hrd_user in hrd_users:
            NotificationHelper.notify_hrd_pending_leave(
                hrd_user.id,
                leave_request.id,
                leave_request.employee.full_name if leave_request.employee else 'Karyawan'
            )
    
    flash('Pengajuan berhasil disetujui', 'success')
    return redirect(url_for('leave.index'))

@leave_bp.route('/<int:leave_id>/reject', methods=['POST'])
@login_required
@supervisor_required
def reject(leave_id):
    """Reject pengajuan"""
    leave_request = LeaveRequest.query.get_or_404(leave_id)
    role = session.get('role')
    user_id = session.get('user_id')
    rejection_reason = request.form.get('rejection_reason', '')
    
    leave_request.status = 'ditolak'
    leave_request.rejection_reason = rejection_reason
    
    if role == 'atasan':
        leave_request.supervisor_approval = False
    elif role in ['admin', 'hrd']:
        leave_request.hrd_approval = False
        leave_request.hrd_id = user_id
    
    db.session.commit()
    
    # Log audit
    AuditLogger.log_data_change(
        user_id,
        session.get('username'),
        'reject',
        'leave_requests',
        leave_request.id,
        f'Rejected {leave_request.leave_type} request'
    )
    
    # Create notification
    NotificationHelper.notify_leave_approval(
        User.query.filter_by(employee_id=leave_request.employee_id).first().id,
        leave_request.id,
        False,
        leave_request.leave_type
    )
    
    flash('Pengajuan ditolak', 'info')
    return redirect(url_for('leave.index'))
