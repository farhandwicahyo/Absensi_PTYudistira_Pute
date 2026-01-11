"""
Model AuditLog untuk audit log dan riwayat aktivitas
"""
from datetime import datetime
from models import db

class AuditLog(db.Model):
    """Model untuk audit log aktivitas sistem"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    username = db.Column(db.String(50), nullable=True)
    activity = db.Column(db.String(100), nullable=False)  # login, logout, presensi, dll
    action = db.Column(db.String(50), nullable=False)  # create, update, delete, view
    table_name = db.Column(db.String(50), nullable=True)
    record_id = db.Column(db.Integer, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    details = db.Column(db.Text, nullable=True)  # JSON atau text detail
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    user = db.relationship('User', backref='audit_logs')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'activity': self.activity,
            'action': self.action,
            'table_name': self.table_name,
            'record_id': self.record_id,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
