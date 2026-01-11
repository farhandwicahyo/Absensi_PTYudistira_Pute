"""
Controller untuk lembur
"""
from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from models import db
from models.overtime import Overtime
from models.employee import Employee
from models.user import User
from utils.decorators import login_required, supervisor_required
from utils.audit_logger import AuditLogger
from utils.notification_helper import NotificationHelper
from datetime import datetime, timedelta

overtime_bp = Blueprint('overtime', __name__)

@overtime_bp.route('/')
@login_required
def index():
    """Daftar pengajuan lembur"""
    role = session.get('role')
    employee_id = session.get('employee_id')
    
    query = Overtime.query
    
    if role == 'karyawan':
        query = query.filter_by(employee_id=employee_id)
    elif role == 'atasan':
        # Show subordinates' requests
        employee = Employee.query.get(employee_id)
        if employee:
            subordinate_ids = [e.id for e in employee.subordinates]
            query = query.filter(Overtime.employee_id.in_(subordinate_ids))
    
    overtimes = query.order_by(Overtime.overtime_date.desc()).all()
    
    return render_template('overtime/index.html', overtimes=overtimes, role=role)

@overtime_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Buat pengajuan lembur"""
    employee_id = session.get('employee_id')
    
    if request.method == 'POST':
        overtime_date = request.form.get('overtime_date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        reason = request.form.get('reason')
        
        # Get employee to find supervisor
        employee = Employee.query.get(employee_id)
        if not employee:
            flash('Data karyawan tidak ditemukan', 'error')
            return redirect(url_for('overtime.index'))
        
        # Calculate total hours
        start = datetime.strptime(start_time, '%H:%M').time()
        end = datetime.strptime(end_time, '%H:%M').time()
        
        start_dt = datetime.combine(datetime.today(), start)
        end_dt = datetime.combine(datetime.today(), end)
        if end_dt < start_dt:
            end_dt += timedelta(days=1)
        
        total_hours = (end_dt - start_dt).total_seconds() / 3600
        
        # Create overtime request
        overtime = Overtime(
            employee_id=employee_id,
            overtime_date=datetime.strptime(overtime_date, '%Y-%m-%d').date(),
            start_time=start,
            end_time=end,
            total_hours=total_hours,
            reason=reason,
            supervisor_id=employee.supervisor_id
        )
        
        db.session.add(overtime)
        db.session.commit()
        
        # Log audit
        AuditLogger.log_data_change(
            session.get('user_id'),
            session.get('username'),
            'create',
            'overtimes',
            overtime.id,
            f'Created overtime request: {total_hours} hours'
        )
        
        # Create notification
        NotificationHelper.notify_overtime_submitted(
            session.get('user_id'),
            overtime.id
        )
        
        flash('Pengajuan lembur berhasil dikirim', 'success')
        return redirect(url_for('overtime.index'))
    
    return render_template('overtime/create.html')

@overtime_bp.route('/<int:overtime_id>/approve', methods=['POST'])
@login_required
@supervisor_required
def approve(overtime_id):
    """Approve pengajuan lembur"""
    overtime = Overtime.query.get_or_404(overtime_id)
    role = session.get('role')
    user_id = session.get('user_id')
    
    # Check if can approve
    if role == 'atasan':
        if overtime.supervisor_id != session.get('employee_id'):
            flash('Anda tidak berhak menyetujui pengajuan ini', 'error')
            return redirect(url_for('overtime.index'))
        
        overtime.supervisor_approval = True
        overtime.supervisor_approval_date = datetime.utcnow()
        
        if not overtime.hrd_approval:
            pass
        else:
            overtime.status = 'disetujui'
    
    elif role in ['admin', 'hrd']:
        overtime.hrd_approval = True
        overtime.hrd_approval_date = datetime.utcnow()
        overtime.hrd_id = user_id
        
        if overtime.supervisor_approval:
            overtime.status = 'disetujui'
    
    db.session.commit()
    
    # Log audit
    AuditLogger.log_data_change(
        user_id,
        session.get('username'),
        'approve',
        'overtimes',
        overtime.id,
        'Approved overtime request'
    )
    
    # Create notification
    NotificationHelper.notify_overtime_approval(
        User.query.filter_by(employee_id=overtime.employee_id).first().id,
        overtime.id,
        True
    )
    
    flash('Pengajuan lembur berhasil disetujui', 'success')
    return redirect(url_for('overtime.index'))

@overtime_bp.route('/<int:overtime_id>/reject', methods=['POST'])
@login_required
@supervisor_required
def reject(overtime_id):
    """Reject pengajuan lembur"""
    overtime = Overtime.query.get_or_404(overtime_id)
    role = session.get('role')
    user_id = session.get('user_id')
    rejection_reason = request.form.get('rejection_reason', '')
    
    overtime.status = 'ditolak'
    overtime.rejection_reason = rejection_reason
    
    if role == 'atasan':
        overtime.supervisor_approval = False
    elif role in ['admin', 'hrd']:
        overtime.hrd_approval = False
        overtime.hrd_id = user_id
    
    db.session.commit()
    
    # Log audit
    AuditLogger.log_data_change(
        user_id,
        session.get('username'),
        'reject',
        'overtimes',
        overtime.id,
        'Rejected overtime request'
    )
    
    # Create notification
    NotificationHelper.notify_overtime_approval(
        User.query.filter_by(employee_id=overtime.employee_id).first().id,
        overtime.id,
        False
    )
    
    flash('Pengajuan lembur ditolak', 'info')
    return redirect(url_for('overtime.index'))
