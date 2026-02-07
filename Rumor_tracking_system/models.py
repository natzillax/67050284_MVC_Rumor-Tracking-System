from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Rumour(db.Model):
    id = db.Column(db.Integer, primary_key=True) # เลข 8 หลัก
    title = db.Column(db.String(200), nullable=False)
    source = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    credibility_score = db.Column(db.Integer, default=50)
    status = db.Column(db.String(20), default='ปกติ') # ปกติ / panic

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20)) # ผู้ใช้ทั่วไป / ผู้ตรวจสอบ

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rumour_id = db.Column(db.Integer, db.ForeignKey('rumour.id'))
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)
    report_type = db.Column(db.String(50)) # บิดเบือน / ปลุกปั่น / ข้อมูลเท็จ