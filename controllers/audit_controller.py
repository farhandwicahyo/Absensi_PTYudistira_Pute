"""
Controller untuk audit log
"""
from flask import Blueprint, render_template, request, session
from models.audit_log import AuditLog
from utils.decorators import login_required, admin_required
from datetime import datetime

audit_bp = Blueprint('audit', __name__)

@audit_bp.route('/')
@login_required
@admin_required
def index():
    """Daftar audit log"""
    # Get filter parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    activity = request.args.get('activity')
    
    query = AuditLog.query
    
    # Date filter
    if start_date:
        query = query.filter(AuditLog.created_at >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(AuditLog.created_at <= datetime.strptime(end_date, '%Y-%m-%d'))
    
    # Activity filter
    if activity:
        query = query.filter(AuditLog.activity == activity)
    
    logs = query.order_by(AuditLog.created_at.desc()).limit(1000).all()
    
    return render_template('audit/index.html', logs=logs)
