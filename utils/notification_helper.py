"""
Helper untuk membuat notifikasi
"""
from models import db
from models.notification import Notification
from datetime import datetime

class NotificationHelper:
    """Helper class untuk membuat notifikasi"""
    
    @staticmethod
    def create_notification(user_id, title, message, notification_type, related_id=None):
        """Membuat notifikasi baru"""
        try:
            notification = Notification(
                user_id=user_id,
                title=title,
                message=message,
                notification_type=notification_type,
                related_id=related_id
            )
            db.session.add(notification)
            db.session.commit()
            return notification
        except Exception as e:
            db.session.rollback()
            print(f"Error creating notification: {str(e)}")
            return None
    
    @staticmethod
    def notify_presensi_success(user_id, attendance_id):
        """Notifikasi presensi berhasil"""
        NotificationHelper.create_notification(
            user_id=user_id,
            title='Presensi Berhasil',
            message='Presensi Anda telah berhasil dicatat.',
            notification_type='presensi',
            related_id=attendance_id
        )
    
    @staticmethod
    def notify_presensi_failed(user_id, reason):
        """Notifikasi presensi gagal"""
        NotificationHelper.create_notification(
            user_id=user_id,
            title='Presensi Gagal',
            message=f'Presensi gagal: {reason}',
            notification_type='presensi'
        )
    
    @staticmethod
    def notify_leave_submitted(user_id, leave_request_id, leave_type):
        """Notifikasi pengajuan izin/cuti/sakit"""
        NotificationHelper.create_notification(
            user_id=user_id,
            title=f'Pengajuan {leave_type.capitalize()} Dikirim',
            message=f'Pengajuan {leave_type} Anda telah dikirim dan menunggu persetujuan.',
            notification_type='leave',
            related_id=leave_request_id
        )
    
    @staticmethod
    def notify_leave_approval(user_id, leave_request_id, approved, leave_type, approver_role=''):
        """Notifikasi persetujuan izin/cuti/sakit"""
        status = 'disetujui' if approved else 'ditolak'
        approver_text = f' oleh {approver_role}' if approver_role else ''
        NotificationHelper.create_notification(
            user_id=user_id,
            title=f'Pengajuan {leave_type.capitalize()} {status.capitalize()}',
            message=f'Pengajuan {leave_type} Anda telah {status}{approver_text}.',
            notification_type='leave',
            related_id=leave_request_id
        )
    
    @staticmethod
    def notify_supervisor_new_leave(user_id, leave_request_id, leave_type, employee_name):
        """Notifikasi untuk atasan tentang pengajuan baru dari bawahan"""
        NotificationHelper.create_notification(
            user_id=user_id,
            title=f'Pengajuan {leave_type.capitalize()} Baru',
            message=f'{employee_name} mengajukan {leave_type}. Silakan review dan approve.',
            notification_type='leave',
            related_id=leave_request_id
        )
    
    @staticmethod
    def notify_hrd_pending_leave(user_id, leave_request_id, employee_name):
        """Notifikasi untuk HRD tentang pengajuan cuti yang sudah di-approve atasan"""
        NotificationHelper.create_notification(
            user_id=user_id,
            title='Pengajuan Cuti Menunggu Approval HRD',
            message=f'Pengajuan cuti dari {employee_name} telah disetujui atasan dan menunggu approval HRD.',
            notification_type='leave',
            related_id=leave_request_id
        )
    
    @staticmethod
    def notify_overtime_submitted(user_id, overtime_id):
        """Notifikasi pengajuan lembur"""
        NotificationHelper.create_notification(
            user_id=user_id,
            title='Pengajuan Lembur Dikirim',
            message='Pengajuan lembur Anda telah dikirim dan menunggu persetujuan.',
            notification_type='overtime',
            related_id=overtime_id
        )
    
    @staticmethod
    def notify_overtime_approval(user_id, overtime_id, approved):
        """Notifikasi persetujuan lembur"""
        status = 'disetujui' if approved else 'ditolak'
        NotificationHelper.create_notification(
            user_id=user_id,
            title=f'Pengajuan Lembur {status.capitalize()}',
            message=f'Pengajuan lembur Anda telah {status}.',
            notification_type='overtime',
            related_id=overtime_id
        )
