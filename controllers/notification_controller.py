"""
Controller untuk notifikasi
"""
from flask import Blueprint, jsonify, session, request
from models import db
from models.notification import Notification
from utils.decorators import login_required

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/')
@login_required
def index():
    """Daftar notifikasi"""
    user_id = session.get('user_id')
    notifications = Notification.query.filter_by(
        user_id=user_id
    ).order_by(Notification.created_at.desc()).limit(50).all()
    
    return jsonify([n.to_dict() for n in notifications])

@notification_bp.route('/unread')
@login_required
def unread():
    """Notifikasi yang belum dibaca"""
    user_id = session.get('user_id')
    notifications = Notification.query.filter_by(
        user_id=user_id,
        is_read=False
    ).order_by(Notification.created_at.desc()).all()
    
    return jsonify([n.to_dict() for n in notifications])

@notification_bp.route('/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_read(notification_id):
    """Tandai notifikasi sebagai sudah dibaca"""
    user_id = session.get('user_id')
    notification = Notification.query.get_or_404(notification_id)
    
    if notification.user_id != user_id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    notification.is_read = True
    db.session.commit()
    
    return jsonify({'success': True})

@notification_bp.route('/read-all', methods=['POST'])
@login_required
def mark_all_read():
    """Tandai semua notifikasi sebagai sudah dibaca"""
    user_id = session.get('user_id')
    Notification.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
    db.session.commit()
    
    return jsonify({'success': True})
