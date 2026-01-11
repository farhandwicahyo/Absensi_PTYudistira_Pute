"""
Controller untuk dashboard
"""
from flask import Blueprint, render_template, session
from models import db
from models.attendance import Attendance
from models.leave_request import LeaveRequest
from models.overtime import Overtime
from models.notification import Notification
from models.employee import Employee
from utils.decorators import login_required
from datetime import datetime, date, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    """Dashboard utama"""
    user_id = session.get('user_id')
    role = session.get('role')
    employee_id = session.get('employee_id')
    
    # Get statistics based on role
    stats = {}
    
    if role == 'karyawan':
        # Stats for employee
        today = date.today()
        today_attendance = Attendance.query.filter_by(
            employee_id=employee_id,
            attendance_date=today
        ).first()
        
        stats['today_attendance'] = today_attendance
        stats['pending_leaves'] = LeaveRequest.query.filter_by(
            employee_id=employee_id,
            status='menunggu'
        ).count()
        stats['pending_overtimes'] = Overtime.query.filter_by(
            employee_id=employee_id,
            status='menunggu'
        ).count()
        
        # Recent notifications
        notifications = Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).order_by(Notification.created_at.desc()).limit(5).all()
        
    elif role in ['admin', 'hrd']:
        # Stats for admin/HRD
        stats['total_employees'] = Employee.query.filter_by(status='aktif').count()
        stats['today_attendances'] = Attendance.query.filter_by(
            attendance_date=date.today()
        ).count()
        stats['pending_leaves'] = LeaveRequest.query.filter_by(
            status='menunggu'
        ).count()
        stats['pending_overtimes'] = Overtime.query.filter_by(
            status='menunggu'
        ).count()
        
        # Recent notifications
        notifications = Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).order_by(Notification.created_at.desc()).limit(5).all()
        
    elif role == 'atasan':
        # Stats for supervisor
        employee = Employee.query.get(employee_id)
        subordinate_ids = [e.id for e in employee.subordinates] if employee else []
        
        stats['subordinates'] = len(subordinate_ids)
        stats['pending_leaves'] = LeaveRequest.query.filter(
            LeaveRequest.supervisor_id == employee_id,
            LeaveRequest.status == 'menunggu'
        ).count()
        stats['pending_overtimes'] = Overtime.query.filter(
            Overtime.supervisor_id == employee_id,
            Overtime.status == 'menunggu'
        ).count()
        
        # Recent notifications
        notifications = Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).order_by(Notification.created_at.desc()).limit(5).all()
    
    return render_template('dashboard/index.html', stats=stats, notifications=notifications, role=role)
