"""
Model Overtime untuk lembur
"""
from datetime import datetime
from models import db

class Overtime(db.Model):
    """Model untuk pengajuan dan pencatatan lembur"""
    __tablename__ = 'overtimes'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    overtime_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    total_hours = db.Column(db.Float, nullable=False)
    reason = db.Column(db.Text, nullable=False)
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
    employee = db.relationship('Employee', foreign_keys=[employee_id], backref='overtimes')
    supervisor = db.relationship('Employee', foreign_keys=[supervisor_id])
    hrd_user = db.relationship('User', foreign_keys=[hrd_id])
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.full_name if self.employee else None,
            'overtime_date': self.overtime_date.isoformat() if self.overtime_date else None,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'total_hours': self.total_hours,
            'reason': self.reason,
            'status': self.status,
            'supervisor_approval': self.supervisor_approval,
            'hrd_approval': self.hrd_approval,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
