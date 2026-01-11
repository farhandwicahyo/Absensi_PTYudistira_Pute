"""
Model LeaveRequest untuk pengajuan izin, cuti, dan sakit
"""
from datetime import datetime
from models import db

class LeaveRequest(db.Model):
    """Model untuk pengajuan izin, cuti, dan sakit"""
    __tablename__ = 'leave_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    leave_type = db.Column(db.String(20), nullable=False)  # izin, cuti, sakit
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    attachment_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='menunggu')  # menunggu, disetujui, ditolak
    supervisor_approval = db.Column(db.Boolean, default=False)
    supervisor_approval_date = db.Column(db.DateTime, nullable=True)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    hrd_approval = db.Column(db.Boolean, default=False)
    hrd_approval_date = db.Column(db.DateTime, nullable=True)
    hrd_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    employee = db.relationship('Employee', foreign_keys=[employee_id], backref='leave_requests')
    supervisor = db.relationship('Employee', foreign_keys=[supervisor_id])
    hrd_user = db.relationship('User', foreign_keys=[hrd_id])
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.full_name if self.employee else None,
            'leave_type': self.leave_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'reason': self.reason,
            'status': self.status,
            'supervisor_approval': self.supervisor_approval,
            'hrd_approval': self.hrd_approval,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
