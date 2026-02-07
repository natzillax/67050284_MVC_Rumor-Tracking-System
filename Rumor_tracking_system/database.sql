
CREATE TABLE rumour (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    source TEXT,
    created_at DATETIME,
    credibility_score INTEGER,
    status TEXT -- ปกติ / panic 
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT -- ผู้ใช้ทั่วไป / ผู้ตรวจสอบ 
);

CREATE TABLE report (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    rumour_id INTEGER,
    reported_at DATETIME,
    report_type TEXT, -- บิดเบือน / ปลุกปั่น / ข้อมูลเท็จ 
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(rumour_id) REFERENCES rumour(id)
);