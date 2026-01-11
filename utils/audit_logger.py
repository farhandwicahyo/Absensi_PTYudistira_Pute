"""
Utility untuk audit logging
"""
from flask import request
from models import db
from models.audit_log import AuditLog
from datetime import datetime

class AuditLogger:
    """Class untuk logging aktivitas ke audit log"""
    
    @staticmethod
    def log(user_id, username, activity, action, table_name=None, record_id=None, details=None):
        """Membuat log aktivitas"""
        try:
            log = AuditLog(
                user_id=user_id,
                username=username,
                activity=activity,
                action=action,
                table_name=table_name,
                record_id=record_id,
                ip_address=request.remote_addr if request else None,
                user_agent=request.headers.get('User-Agent') if request else None,
                details=details
            )
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error logging audit: {str(e)}")
    
    @staticmethod
    def log_login(user_id, username, success=True):
        """Log aktivitas login"""
        action = 'login_success' if success else 'login_failed'
        AuditLogger.log(user_id, username, 'login', action)
    
    @staticmethod
    def log_logout(user_id, username):
        """Log aktivitas logout"""
        AuditLogger.log(user_id, username, 'logout', 'logout')
    
    @staticmethod
    def log_presensi(user_id, username, action, attendance_id, details=None):
        """Log aktivitas presensi"""
        AuditLogger.log(user_id, username, 'presensi', action, 'attendances', attendance_id, details)
    
    @staticmethod
    def log_data_change(user_id, username, action, table_name, record_id, details=None):
        """Log perubahan data"""
        AuditLogger.log(user_id, username, 'data_change', action, table_name, record_id, details)
