"""
Controller untuk dashboard
"""
from flask import Blueprint, render_template, session, request
from models import db
from models.attendance import Attendance
from models.leave_request import LeaveRequest
from models.overtime import Overtime
from models.notification import Notification
from models.employee import Employee
from utils.decorators import login_required
from datetime import datetime, date, timedelta, time

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
        
        # Recent notifications with date filter
        notification_query = Notification.query.filter_by(user_id=user_id)
        
        # Get date filter from request, default to today
        filter_date = request.args.get('notification_date')
        if not filter_date:
            filter_date = date.today().strftime('%Y-%m-%d')
        
        try:
            filter_date_obj = datetime.strptime(filter_date, '%Y-%m-%d').date()
            # SQL Server compatible: filter by date range instead of using date() function
            start_datetime = datetime.combine(filter_date_obj, time(0, 0, 0))
            end_datetime = datetime.combine(filter_date_obj, time(23, 59, 59))
            notification_query = notification_query.filter(
                Notification.created_at >= start_datetime,
                Notification.created_at <= end_datetime
            )
        except ValueError:
            pass
        
        notifications = notification_query.order_by(Notification.created_at.desc()).limit(10).all()
        
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
        
        # Recent notifications with date filter
        notification_query = Notification.query.filter_by(user_id=user_id)
        
        # Get date filter from request, default to today
        filter_date = request.args.get('notification_date')
        if not filter_date:
            filter_date = date.today().strftime('%Y-%m-%d')
        
        try:
            filter_date_obj = datetime.strptime(filter_date, '%Y-%m-%d').date()
            # SQL Server compatible: filter by date range instead of using date() function
            start_datetime = datetime.combine(filter_date_obj, time(0, 0, 0))
            end_datetime = datetime.combine(filter_date_obj, time(23, 59, 59))
            notification_query = notification_query.filter(
                Notification.created_at >= start_datetime,
                Notification.created_at <= end_datetime
            )
        except ValueError:
            pass
        
        notifications = notification_query.order_by(Notification.created_at.desc()).limit(10).all()
        
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
        
        # Recent notifications with date filter
        notification_query = Notification.query.filter_by(user_id=user_id)
        
        # Get date filter from request, default to today
        filter_date = request.args.get('notification_date')
        if not filter_date:
            filter_date = date.today().strftime('%Y-%m-%d')
        
        try:
            filter_date_obj = datetime.strptime(filter_date, '%Y-%m-%d').date()
            # SQL Server compatible: filter by date range instead of using date() function
            start_datetime = datetime.combine(filter_date_obj, time(0, 0, 0))
            end_datetime = datetime.combine(filter_date_obj, time(23, 59, 59))
            notification_query = notification_query.filter(
                Notification.created_at >= start_datetime,
                Notification.created_at <= end_datetime
            )
        except ValueError:
            pass
        
        notifications = notification_query.order_by(Notification.created_at.desc()).limit(10).all()
    
    # Default to today's date if no filter is set
    filter_date_param = request.args.get('notification_date', '')
    if not filter_date_param:
        filter_date = date.today().strftime('%Y-%m-%d')
        is_default_date = True
    else:
        filter_date = filter_date_param
        is_default_date = (filter_date == date.today().strftime('%Y-%m-%d'))
    
    return render_template('dashboard/index.html', stats=stats, notifications=notifications, role=role, filter_date=filter_date, is_default_date=is_default_date)
