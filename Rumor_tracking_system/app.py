from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Rumour, User, Report
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rumors.db'
app.config['SECRET_KEY'] = 'exit_exam_2568_key'
db.init_app(app)

with app.app_context():
    db.create_all()
    
    # ตรวจสอบและสร้างข้อมูลตัวอย่างตามโจทย์ (User >= 10 คน)
    if not User.query.first():
        u_list = [
            User(id=101, name="สมชาย สายตรวจ", role="ผู้ใช้ทั่วไป"),
            User(id=102, name="มานี มีข่าว", role="ผู้ใช้ทั่วไป"),
            User(id=103, name="ปิติ ดีใจ", role="ผู้ใช้ทั่วไป"),
            User(id=104, name="ชูใจ ไปเรียน", role="ผู้ใช้ทั่วไป"),
            User(id=105, name="วีระ กล้าหาญ", role="ผู้ใช้ทั่วไป"),
            User(id=106, name="ดวงพร สอนดี", role="ผู้ใช้ทั่วไป"),
            User(id=107, name="สมคิด พินิจ", role="ผู้ใช้ทั่วไป"),
            User(id=108, name="สายหยุด หยุดโกหก", role="ผู้ใช้ทั่วไป"),
            User(id=109, name="กนก ยกนิ้ว", role="ผู้ใช้ทั่วไป"),
            User(id=999, name="อาจารย์ตรวจสอบ", role="ผู้ตรวจสอบ")
        ]
        db.session.add_all(u_list)
        db.session.commit()
        print("สร้าง User สำเร็จ")

    # ตรวจสอบและสร้างข้อมูลตัวอย่างข่าวลือ (ข่าวลือ >= 8 ข่าว)
    if not Rumour.query.first():
        r_list = [
            Rumour(id=11110001, title="พรุ่งนี้น้ำมันจะขึ้นราคา 5 บาทต่อลิตร", source="Facebook", credibility_score=40, status="ปกติ"),
            Rumour(id=11110002, title="รัฐบาลประกาศแจกเงินดิจิทัลเพิ่มคนละ 2 หมื่น", source="Twitter/X", credibility_score=20, status="panic"),
            Rumour(id=11110003, title="พบสัตว์ประหลาดในแม่น้ำเจ้าพระยา", source="TikTok", credibility_score=10, status="ปกติ"),
            Rumour(id=11110004, title="ยาชนิดใหม่รักษาโรคมะเร็งหายขาดใน 1 วัน", source="Line Group", credibility_score=15, status="ปกติ"),
            Rumour(id=11110005, title="ห้างดังประกาศปิดตัวทุกสาขาทั่วประเทศ", source="Website", credibility_score=30, status="ปกติ"),
            Rumour(id=11110006, title="เกิดเหตุแผ่นดินไหวรุนแรงใจกลางกรุงเทพฯ", source="Twitter/X", credibility_score=5, status="panic"),
            Rumour(id=11110007, title="ห้ามออกจากบ้านหลังเที่ยงคืนเพราะพายุสุริยะ", source="Facebook", credibility_score=50, status="ปกติ"),
            Rumour(id=11110008, title="ยกเลิกการสอบ Exit Exam ทุกมหาวิทยาลัย", source="เว็บบอร์ด", credibility_score=10, status="ปกติ"),
            Rumour(id=22220001, title="ประกาศผลสอบ Exit Exam ภายใน 7 วัน", source="Official Site", credibility_score=90, status="ข้อมูลจริง"),
            Rumour(id=22220002, title="พบมนุษย์ต่างดาวบุกสยามพารากอน", source="TikTok", credibility_score=0, status="ข้อมูลเท็จ") 
        ]
        db.session.add_all(r_list)
        
        # สร้าง Report ตัวอย่างเพื่อให้ข่าวติดสถานะ Panic ทันที
        reports = [
            Report(user_id=101, rumour_id=11110002, report_type="ข้อมูลเท็จ", reported_at=datetime.now()),
            Report(user_id=102, rumour_id=11110002, report_type="บิดเบือน", reported_at=datetime.now()),
            Report(user_id=103, rumour_id=11110002, report_type="ปลุกปั่น", reported_at=datetime.now()),
        ]
        db.session.add_all(reports)
        db.session.commit()
        print("สร้างข่าวลือและรายงานตัวอย่างสำเร็จ")

# --- Routes (Controller) ---

@app.route('/')
def index():
    """หน้าแรก: หน้ารวมข่าวลือ เรียงตามความร้อนแรง (จำนวนรายงาน)"""
    rumours = Rumour.query.all()
    display_data = []
    for r in rumours:
        report_count = Report.query.filter_by(rumour_id=r.id).count()
        display_data.append({'data': r, 'count': report_count})
    
    # เรียงลำดับจากรายงานมากไปน้อย
    display_data.sort(key=lambda x: x['count'], reverse=True)
    return render_template('index.html', rumours=display_data)

@app.route('/rumour/<int:rid>')
def detail(rid):
    """หน้ารายละเอียดข่าวลือ"""
    rumour = Rumour.query.get_or_404(rid)
    reports_count = Report.query.filter_by(rumour_id=rid).count() 
    return render_template('detail.html', rumour=rumour, reports_count=reports_count)

@app.route('/report/<int:rid>', methods=['POST'])
def submit_report(rid):
    """Action สำหรับการส่งรายงานข่าวลือ (สำหรับ User ทั่วไป)"""
    uid_input = request.form.get('user_id')
    if not uid_input:
        flash("กรุณาระบุรหัสผู้ใช้งาน", "danger")
        return redirect(url_for('detail', rid=rid))
        
    uid = int(uid_input)
    rtype = request.form.get('report_type')
    rumour = Rumour.query.get_or_404(rid)

    # Business Rule: ข่าวที่ตรวจแล้วรายงานเพิ่มไม่ได้
    if rumour.status in ['ข้อมูลจริง', 'ข้อมูลเท็จ']:
        flash("ข่าวนี้ได้รับการตรวจสอบเสร็จสิ้นแล้ว ไม่สามารถส่งรายงานเพิ่มได้", "danger")
        return redirect(url_for('detail', rid=rid))

    # Business Rule: ห้ามผู้ใช้คนเดิมรายงานข่าวเดิมซ้ำ
    existing_report = Report.query.filter_by(user_id=uid, rumour_id=rid).first()
    if existing_report:
        flash("คุณเคยรายงานข่าวนี้ไปแล้ว ระบบไม่อนุญาตให้รายงานซ้ำ", "warning")
        return redirect(url_for('detail', rid=rid))

    # บันทึกรายงาน
    new_report = Report(user_id=uid, rumour_id=rid, report_type=rtype, reported_at=datetime.now())
    db.session.add(new_report)
    
    # Business Rule: ถ้ารายงานรวมสะสม >= 3 ให้ปรับเป็น panic อัตโนมัติ
    total_reports = Report.query.filter_by(rumour_id=rid).count() + 1
    if total_reports >= 3 and rumour.status == 'ปกติ':
        rumour.status = 'panic' 
    
    db.session.commit()
    flash("ส่งรายงานสำเร็จ", "success")
    return redirect(url_for('detail', rid=rid))

@app.route('/summary')
def summary():
    """หน้าสรุปผล: แสดงรายการ Panic และข่าวที่ยืนยันแล้ว"""
    panic_news = Rumour.query.filter(Rumour.status.in_(['panic', 'Panic'])).all() 
    verified_news = Rumour.query.filter(Rumour.status.in_(['ข้อมูลจริง', 'ข้อมูลเท็จ'])).all() 
    return render_template('summary.html', panic=panic_news, verified=verified_news)

@app.route('/verify/<int:rid>', methods=['POST'])
def verify_rumour(rid):
    """ฟังก์ชันสำหรับผู้ตรวจสอบ (Auditor) ในการเปลี่ยนสถานะข่าวลือ"""
    # ดึงรหัสที่กรอกจากฟอร์มมาเช็ก
    auditor_id_input = request.form.get('auditor_id')
    
    # เช็กว่าเป็นเลข 999 หรือไม่ (หรือเช็กจากฐานข้อมูลว่า role == 'ผู้ตรวจสอบ')
    user = User.query.get(auditor_id_input)
    
    if not user or user.role != "ผู้ตรวจสอบ":
        # ถ้าไม่ใช่ผู้ตรวจสอบ ให้ดีดกลับและแจ้งเตือน
        flash("🚫 ปฏิเสธการเข้าถึง: รหัสผู้ใช้ของคุณไม่มีสิทธิ์ในการยืนยันข้อมูล", "danger")
        return redirect(url_for('detail', rid=rid))

    # ถ้าผ่านเงื่อนไข (เป็น Auditor) ถึงจะยอมให้เปลี่ยนสถานะ
    rumour = Rumour.query.get_or_404(rid)
    new_status = request.form.get('new_status') # รับค่าจาก <select>
    
    rumour.status = new_status
    db.session.commit()
    
    flash(f"✅ ดำเนินการสำเร็จ: เปลี่ยนสถานะเป็น {new_status} เรียบร้อยแล้ว", "success")
    return redirect(url_for('detail', rid=rid))

if __name__ == '__main__':
    app.run(debug=True)