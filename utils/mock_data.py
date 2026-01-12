"""
Mock data untuk demo mode (tanpa database)
"""
from datetime import datetime, date, timedelta

class MockAttendance:
    """Mock object untuk Attendance"""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 1)
        self.employee_id = kwargs.get('employee_id', 1)
        self.attendance_date = kwargs.get('attendance_date', date.today())
        self.check_in_time = kwargs.get('check_in_time', datetime.now().replace(hour=7, minute=30))
        self.check_out_time = kwargs.get('check_out_time', datetime.now().replace(hour=17, minute=0))
        self.status = kwargs.get('status', 'hadir')
        self.notes = kwargs.get('notes', None)
        self.employee = kwargs.get('employee', MockEmployee(full_name='John Doe'))
    
    def __getattr__(self, name):
        return None

class MockEmployee:
    """Mock object untuk Employee"""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 1)
        self.nik = kwargs.get('nik', 'EMP001')
        self.full_name = kwargs.get('full_name', 'John Doe')
        self.email = kwargs.get('email', 'john@company.com')
        self.phone = kwargs.get('phone', '081234567890')
        self.position = kwargs.get('position', 'Developer')
        self.division = kwargs.get('division', 'IT')
        self.status = kwargs.get('status', 'aktif')
        self.supervisor_id = kwargs.get('supervisor_id', None)
        self.subordinates = kwargs.get('subordinates', [])

class MockLeaveRequest:
    """Mock object untuk LeaveRequest"""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 1)
        self.employee_id = kwargs.get('employee_id', 1)
        self.leave_type = kwargs.get('leave_type', 'izin')
        self.start_date = kwargs.get('start_date', date.today())
        self.end_date = kwargs.get('end_date', date.today())
        self.reason = kwargs.get('reason', 'Keperluan keluarga')
        self.status = kwargs.get('status', 'menunggu')
        self.supervisor_approval = kwargs.get('supervisor_approval', False)
        self.hrd_approval = kwargs.get('hrd_approval', False)
        self.supervisor_id = kwargs.get('supervisor_id', None)
        self.employee = kwargs.get('employee', MockEmployee())
        self.approval_stage = kwargs.get('approval_stage', 'menunggu_atasan')
        self.created_at = kwargs.get('created_at', datetime.now())

class MockOvertime:
    """Mock object untuk Overtime"""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 1)
        self.employee_id = kwargs.get('employee_id', 1)
        self.overtime_date = kwargs.get('overtime_date', date.today())
        self.start_time = kwargs.get('start_time', datetime.now().replace(hour=18, minute=0).time())
        self.end_time = kwargs.get('end_time', datetime.now().replace(hour=22, minute=0).time())
        self.total_hours = kwargs.get('total_hours', 4.0)
        self.reason = kwargs.get('reason', 'Menyelesaikan project')
        self.status = kwargs.get('status', 'menunggu')
        self.supervisor_approval = kwargs.get('supervisor_approval', False)
        self.hrd_approval = kwargs.get('hrd_approval', False)
        self.employee = kwargs.get('employee', MockEmployee())
        self.created_at = kwargs.get('created_at', datetime.now())

class MockNotification:
    """Mock object untuk Notification"""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 1)
        self.user_id = kwargs.get('user_id', 1)
        self.title = kwargs.get('title', 'Notifikasi')
        self.message = kwargs.get('message', 'Pesan notifikasi')
        self.notification_type = kwargs.get('notification_type', 'system')
        self.is_read = kwargs.get('is_read', False)
        self.related_id = kwargs.get('related_id', None)
        self.created_at = kwargs.get('created_at', datetime.now())

class MockAuditLog:
    """Mock object untuk AuditLog"""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 1)
        self.user_id = kwargs.get('user_id', 1)
        self.username = kwargs.get('username', 'admin')
        self.activity = kwargs.get('activity', 'login')
        self.action = kwargs.get('action', 'login_success')
        self.table_name = kwargs.get('table_name', None)
        self.record_id = kwargs.get('record_id', None)
        self.ip_address = kwargs.get('ip_address', '192.168.1.1')
        self.created_at = kwargs.get('created_at', datetime.now())

def get_mock_attendances(count=10):
    """Generate mock attendances"""
    attendances = []
    for i in range(count):
        att_date = date.today() - timedelta(days=i)
        check_in = datetime.now().replace(hour=7, minute=30+i%30)
        check_out = datetime.now().replace(hour=17, minute=0) if i % 2 == 0 else None
        status = ['hadir', 'terlambat', 'pulang_cepat'][i % 3]
        
        att = MockAttendance(
            id=i+1,
            employee_id=1,
            attendance_date=att_date,
            check_in_time=check_in,
            check_out_time=check_out,
            status=status,
            employee=MockEmployee(full_name='John Doe')
        )
        attendances.append(att)
    return attendances

def get_mock_employees(count=10):
    """Generate mock employees"""
    employees = []
    positions = ['Developer', 'Designer', 'Manager', 'Analyst', 'Tester']
    divisions = ['IT', 'Design', 'HRD', 'Finance', 'Marketing']
    
    for i in range(count):
        emp = MockEmployee(
            id=i+1,
            nik=f'EMP{i+1:03d}',
            full_name=f'Employee {i+1}',
            email=f'emp{i+1}@company.com',
            phone=f'0812345678{i:02d}',
            position=positions[i % len(positions)],
            division=divisions[i % len(divisions)],
            status='aktif' if i < 8 else 'nonaktif'
        )
        employees.append(emp)
    return employees

def get_mock_leave_requests(count=5):
    """Generate mock leave requests"""
    requests = []
    leave_types = ['izin', 'cuti', 'sakit']
    statuses = ['menunggu', 'menunggu_hrd', 'disetujui', 'ditolak']
    
    for i in range(count):
        status = statuses[i % len(statuses)]
        req = MockLeaveRequest(
            id=i+1,
            employee_id=1,
            leave_type=leave_types[i % len(leave_types)],
            start_date=date.today() + timedelta(days=i),
            end_date=date.today() + timedelta(days=i+1),
            reason=f'Alasan pengajuan {i+1}',
            status=status,
            employee=MockEmployee(full_name=f'Employee {i+1}'),
            supervisor_id=2 if status == 'menunggu' else None,  # Ada supervisor untuk yang menunggu
            approval_stage='menunggu_atasan' if status == 'menunggu' else ('menunggu_hrd' if status == 'menunggu_hrd' else status)
        )
        requests.append(req)
    return requests

def get_mock_overtimes(count=5):
    """Generate mock overtimes"""
    overtimes = []
    for i in range(count):
        ot = MockOvertime(
            id=i+1,
            employee_id=1,
            overtime_date=date.today() + timedelta(days=i),
            total_hours=4.0 + i,
            reason=f'Alasan lembur {i+1}',
            status='menunggu' if i % 2 == 0 else 'disetujui',
            employee=MockEmployee(full_name='John Doe')
        )
        overtimes.append(ot)
    return overtimes

def get_mock_notifications(count=5):
    """Generate mock notifications"""
    notifications = []
    titles = [
        'Presensi Berhasil',
        'Pengajuan Cuti Dikirim',
        'Pengajuan Disetujui',
        'Pengajuan Lembur Dikirim',
        'Notifikasi Sistem'
    ]
    
    for i in range(count):
        notif = MockNotification(
            id=i+1,
            user_id=1,
            title=titles[i % len(titles)],
            message=f'Ini adalah pesan notifikasi {i+1}',
            notification_type=['presensi', 'leave', 'overtime', 'system'][i % 4],
            is_read=i > 2
        )
        notifications.append(notif)
    return notifications

def get_mock_audit_logs(count=20):
    """Generate mock audit logs"""
    logs = []
    activities = ['login', 'logout', 'presensi', 'data_change']
    actions = ['login_success', 'logout', 'check_in', 'check_out', 'create', 'update', 'delete']
    
    for i in range(count):
        log = MockAuditLog(
            id=i+1,
            user_id=1,
            username='admin',
            activity=activities[i % len(activities)],
            action=actions[i % len(actions)],
            table_name='employees' if i % 2 == 0 else 'attendances',
            record_id=i+1,
            created_at=datetime.now() - timedelta(hours=i)
        )
        logs.append(log)
    return logs
