"""
Model Attendance untuk presensi
"""
from datetime import datetime, date
from models import db

class Attendance(db.Model):
    """Model untuk presensi karyawan"""
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False, default=date.today)
    check_in_time = db.Column(db.DateTime, nullable=True)
    check_out_time = db.Column(db.DateTime, nullable=True)
    check_in_latitude = db.Column(db.Float, nullable=True)
    check_in_longitude = db.Column(db.Float, nullable=True)
    check_out_latitude = db.Column(db.Float, nullable=True)
    check_out_longitude = db.Column(db.Float, nullable=True)
    check_in_ip = db.Column(db.String(45), nullable=True)
    check_out_ip = db.Column(db.String(45), nullable=True)
    check_in_browser = db.Column(db.String(100), nullable=True)
    check_out_browser = db.Column(db.String(100), nullable=True)
    check_in_os = db.Column(db.String(50), nullable=True)
    check_out_os = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default='hadir')  # hadir, terlambat, pulang_cepat, alpha
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    employee = db.relationship('Employee', backref='attendances')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.full_name if self.employee else None,
            'attendance_date': self.attendance_date.isoformat() if self.attendance_date else None,
            'check_in_time': self.check_in_time.isoformat() if self.check_in_time else None,
            'check_out_time': self.check_out_time.isoformat() if self.check_out_time else None,
            'status': self.status,
            'notes': self.notes
        }
