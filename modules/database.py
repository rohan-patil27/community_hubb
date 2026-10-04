import sqlite3

DB_PATH = "slum_system.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, age INTEGER, dob TEXT,
        phone TEXT UNIQUE, email TEXT, password TEXT,
        location TEXT, district TEXT, state TEXT DEFAULT 'Maharashtra',
        skills TEXT, education TEXT,
        income INTEGER DEFAULT 0,
        gender TEXT DEFAULT 'Male',
        caste TEXT DEFAULT 'General',
        is_admin INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    for col in ["email TEXT", "state TEXT DEFAULT 'Maharashtra'", "dob TEXT"]:
        try:
            c.execute(f"ALTER TABLE users ADD COLUMN {col}")
        except:
            pass

    c.execute('''CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT, company TEXT, location TEXT, district TEXT,
        required_skills TEXT, min_education TEXT,
        salary_min INTEGER, salary_max INTEGER,
        job_type TEXT, description TEXT, contact TEXT,
        is_verified INTEGER DEFAULT 0,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS schemes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, category TEXT, description TEXT,
        eligibility TEXT, max_age INTEGER, min_age INTEGER DEFAULT 0,
        max_income INTEGER, gender TEXT DEFAULT 'All',
        caste TEXT DEFAULT 'All', benefits TEXT,
        apply_link TEXT, document_required TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS emergency_contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, type TEXT, location TEXT, district TEXT,
        phone TEXT, address TEXT, services TEXT, timing TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, job_id INTEGER,
        applied_at TEXT DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Applied',
        notes TEXT DEFAULT ''
    )''')

    # NEW: Job reviews & ratings
    c.execute('''CREATE TABLE IF NOT EXISTS job_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, job_id INTEGER,
        rating INTEGER, review TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    # NEW: Free courses
    c.execute('''CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT, category TEXT, provider TEXT,
        language TEXT, duration TEXT,
        description TEXT, link TEXT,
        skill_tags TEXT, is_free INTEGER DEFAULT 1
    )''')

    # NEW: Admin Audit Logs
    c.execute('''CREATE TABLE IF NOT EXISTS admin_audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER,
        admin_name TEXT,
        action_type TEXT,
        description TEXT,
        category TEXT DEFAULT 'General',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    # NEW: App persistent settings (e.g. API keys)
    c.execute('''CREATE TABLE IF NOT EXISTS app_settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )''')

    _seed(c)
    conn.commit()
    conn.close()

def get_setting(key, default=''):
    try:
        conn = get_conn()
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS app_settings (key TEXT PRIMARY KEY, value TEXT)")
        c.execute("SELECT value FROM app_settings WHERE key = ?", (key,))
        row = c.fetchone()
        conn.close()
        if row and row['value']:
            return row['value']
    except Exception:
        pass
    return default

def set_setting(key, value):
    try:
        conn = get_conn()
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS app_settings (key TEXT PRIMARY KEY, value TEXT)")
        c.execute("INSERT OR REPLACE INTO app_settings (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
        conn.close()
    except Exception as e:
        print("set_setting error:", e)

def log_admin_action(admin_id, admin_name, action_type, description, category='General'):
    try:
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            INSERT INTO admin_audit_logs (admin_id, admin_name, action_type, description, category)
            VALUES (?,?,?,?,?)
        """, (admin_id, admin_name, action_type, description, category))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Admin audit log error:", e)

def get_user_alerts(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM user_alerts WHERE user_id=? ORDER BY id DESC", (user_id,))
    alerts = [dict(row) for row in c.fetchall()]
    conn.close()
    return alerts

def get_unread_alerts_count(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as count FROM user_alerts WHERE user_id=? AND is_read=0", (user_id,))
    res = c.fetchone()
    conn.close()
    return res['count'] if res else 0

def mark_alert_read(alert_id):
    conn = get_conn()
    conn.execute("UPDATE user_alerts SET is_read=1 WHERE id=?", (alert_id,))
    conn.commit()
    conn.close()

def create_alert(user_id, title, message, alert_type='Job', link_page='jobs'):
    conn = get_conn()
    conn.execute("INSERT INTO user_alerts (user_id, title, message, alert_type, link_page) VALUES (?,?,?,?,?)",
                 (user_id, title, message, alert_type, link_page))
    conn.commit()
    conn.close()

def seed_personalized_alerts(user):
    if not user: return
    user_id = user['id']
    alerts = get_user_alerts(user_id)
    if not alerts:
        district = user.get('district', 'Jalgaon')
        skills = user.get('skills', 'Data Engineering, IT')
        caste = user.get('caste', 'General')
        
        # 1. Job Alert
        create_alert(
            user_id,
            f"💼 New Matching Jobs in {district}!",
            f"3 new openings posted for roles matching your skills ({skills}). Check out local opportunities now!",
            alert_type="Job",
            link_page="jobs"
        )
        
        # 2. Scheme Alert
        create_alert(
            user_id,
            f"🏛️ Government Scheme Eligibility Alert!",
            f"Based on your profile ({caste} category, {district}), you qualify for PM Swanidhi, Chief Minister Skill Scheme, and Ladki Bahin Yojana!",
            alert_type="Scheme",
            link_page="schemes"
        )

        # 3. Application Tracker Alert
        create_alert(
            user_id,
            f"📊 Application Status Update",
            "Your recent application status has been updated to 'Under Review' by the recruitment officer.",
            alert_type="Tracker",
            link_page="tracker"
        )

import os
import requests

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")
FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY", "")

def send_sms(phone, message, sms_type='General', user_id=None):
    # 1. Always log to local database
    try:
        conn = get_conn()
        c = conn.cursor()
        c.execute("INSERT INTO sms_logs (user_id, phone, message, sms_type) VALUES (?,?,?,?)",
                  (user_id, phone, message, sms_type))
        conn.commit()
        conn.close()
    except Exception as e:
        print("SMS log DB error:", e)

    # 2. Send REAL SMS via Twilio if configured
    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER:
        try:
            from twilio.rest import Client
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            target = f"+91{phone}" if not phone.startswith("+") else phone
            client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=target)
            print(f"✅ Real SMS sent via Twilio to {target}")
            return True
        except Exception as err:
            print("Twilio SMS send error:", err)

    # 3. Send REAL SMS via Fast2SMS (Indian SMS Gateway) if configured
    elif FAST2SMS_API_KEY:
        try:
            url = "https://www.fast2sms.com/dev/bulkV2"
            headers = {"authorization": FAST2SMS_API_KEY}
            payload = {
                "route": "q",
                "message": message,
                "language": "english",
                "flash": 0,
                "numbers": phone
            }
            res = requests.post(url, headers=headers, data=payload, timeout=5)
            print("Fast2SMS response:", res.json())
            return True
        except Exception as err:
            print("Fast2SMS send error:", err)

    return True

def _seed(c):
    c.execute("SELECT COUNT(*) FROM users WHERE is_admin=1")
    if c.fetchone()[0] == 0:
        c.execute("""INSERT INTO users (name,age,phone,password,location,district,skills,education,income,gender,caste,is_admin)
                     VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                  ("Admin","30","9999999999","admin123","Pune","Pune","Management","Graduate","50000","Male","General",1))

    c.execute("SELECT COUNT(*) FROM users WHERE is_admin=0")
    if c.fetchone()[0] == 0:
        sample_users = [
            ("Ramesh Kumar","28","9876543210","pass123","Dharavi, Mumbai","Mumbai","electrical,wiring","10th Pass","8000","Male","OBC",0),
            ("Sunita Devi","32","9876543211","pass123","Kurla, Mumbai","Mumbai","stitching,tailoring","8th Pass","5000","Female","SC",0),
            ("Mukesh Yadav","22","9876543212","pass123","Nagpur Slum","Nagpur","mobile repair,electronics","10th Pass","0","Male","OBC",0),
            ("Kavita More","45","9876543213","pass123","Thane West","Thane","cleaning,cooking","No education","3000","Female","SC",0),
            ("Arjun Patil","19","9876543214","pass123","Chhatrapati Sambhajinagar","Chhatrapati Sambhajinagar","carpentry,furniture","8th Pass","0","Male","General",0),
        ]
        c.executemany("""INSERT INTO users (name,age,phone,password,location,district,skills,education,income,gender,caste,is_admin)
                         VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", sample_users)

    c.execute("SELECT COUNT(*) FROM jobs")
    if c.fetchone()[0] == 0:
        jobs = [
            ("Electrician","PowerTech Solutions","Dharavi, Mumbai","Mumbai","electrical,wiring,circuits","10th Pass",12000,18000,"Full-time","Experienced electrician needed for residential & commercial work. Immediate joining.","📞 8888811111",1),
            ("Tailor / Stitching Worker","Fashion Hub","Kurla, Mumbai","Mumbai","stitching,tailoring,sewing","8th Pass",8000,14000,"Full-time","Stitching work in garment factory. Bonus for fast workers.","📞 7777722222",1),
            ("Hospital Helper / Peon","City Hospital","Nagpur","Nagpur","cleaning,helping,basic work","No education",7500,10000,"Full-time","Hospital helper for cleaning and patient assistance.","📞 9999933333",1),
            ("Mobile Repair Technician","QuickFix Mobile","Chhatrapati Sambhajinagar","Chhatrapati Sambhajinagar","mobile repair,electronics,hardware","10th Pass",10000,20000,"Full-time","Smartphone & tablet repair. Training provided.","📞 8888844444",1),
            ("Security Guard","Safe Secure Pvt Ltd","Thane","Thane","security,patrolling,vigilance","10th Pass",9000,13000,"Full-time","Night shift security guard for residential complex.","📞 7777755555",1),
            ("Carpenter","WoodWork Enterprises","Pune","Pune","carpentry,furniture,woodwork","No education",11000,17000,"Full-time","Skilled carpenter for furniture making.","📞 9966554433",1),
            ("Domestic Cook","HomeChef Services","Mumbai","Mumbai","cooking,cleaning,household","No education",10000,15000,"Full-time","Cook for family. Accommodation provided.","📞 9845612378",0),
            ("Plumber","BuildRight Contractors","Nashik","Nashik","plumbing,pipe fitting,repair","8th Pass",10000,16000,"Full-time","Plumbing work for new construction projects.","📞 9712345678",1),
            ("Auto Rickshaw Driver","City Cab","Pune","Pune","driving,navigation,vehicle","No education",12000,20000,"Full-time","Auto driver with valid licence. Incentive on rides.","📞 9823456789",0),
            ("Data Entry Operator","InfoTech BPO","Mumbai","Mumbai","computer,typing,ms office","12th Pass",12000,18000,"Full-time","Data entry work from office. Basic computer knowledge must.","📞 9012345678",1),
            ("Painter","ColorPro","Thane","Thane","painting,wall painting,color mixing","No education",9000,15000,"Part-time","Residential painting work. Materials provided.","📞 9134567890",0),
            ("Delivery Boy","SwiftDeliver","Nagpur","Nagpur","driving,delivery,navigation","8th Pass",10000,18000,"Full-time","Two-wheeler delivery executive. Bike & licence required.","📞 9945678901",1),
            ("Junior Data Engineer", "TechData Systems", "Sudhakar Nagar, Jalgaon", "Jalgaon", "Data Engineer, SQL, Python, ETL, Data Warehousing, Data Pipelines", "Graduate", 35000, 55000, "Full-time", "Design and build scalable data pipelines, SQL transformations, and data models for analytics.", "📞 9822011223", 1),
            ("Data Scientist / AI Engineer", "NeuroAI Labs", "Hinjewadi, Pune", "Pune", "Data Scientist, Data Science, Machine Learning, Python, AI Engineer, Artificial Intelligence, ML Engineer", "Graduate", 45000, 75000, "Full-time", "Build machine learning & AI models for predictive analytics and natural language processing.", "📞 9833022334", 1),
            ("Software Engineer / Full Stack Developer", "CloudScale Solutions", "Andheri East, Mumbai", "Mumbai", "Software Engineer, Software Developer, Full Stack Developer, Python, JavaScript, HTML, CSS, React, Web Development", "Graduate", 40000, 65000, "Full-time", "Develop responsive web applications, REST APIs, and modern cloud backend services.", "📞 9844033445", 1),
            ("Frontend Web Developer", "WebCraft Studio", "Baner, Pune", "Pune", "Frontend Developer, Web Developer, HTML, CSS, JavaScript, Web Development", "Graduate", 25000, 42000, "Full-time", "Create interactive UI components, mobile responsive layouts, and integrate REST APIs.", "📞 9844099887", 1),
            ("Backend Python Developer", "CoreCode Tech", "Powai, Mumbai", "Mumbai", "Backend Developer, Python, SQL, Git/GitHub, Data Structures", "Graduate", 35000, 60000, "Full-time", "Build secure microservices, REST APIs, and database integrations in Python.", "📞 9844077665", 1),
            ("Mobile App Developer (Android/iOS)", "AppSphere Technologies", "Chhatrapati Sambhajinagar", "Chhatrapati Sambhajinagar", "Mobile App Developer, App Development, Java, JavaScript, Web Development", "Graduate", 30000, 50000, "Full-time", "Develop high performance mobile applications for Android and iOS devices.", "📞 9855011223", 1),
            ("DevOps & Cloud Engineer", "SkyNet Cloud Infra", "Navi Mumbai", "Mumbai", "DevOps Engineer, Cloud Engineer, Cloud Architect, Cloud Computing, Cybersecurity, Networking, Git/GitHub", "Graduate", 50000, 85000, "Work From Home", "Manage AWS/GCP infrastructure, CI/CD pipelines, Docker containers, and Kubernetes.", "📞 9899088990", 1),
            ("Cybersecurity & Network Engineer", "SecureGuard Tech", "Wagle Estate, Thane", "Thane", "Cybersecurity Engineer, Network Engineer, Cybersecurity, Networking, SQL", "Graduate", 38000, 62000, "Full-time", "Penetration testing, network security monitoring, firewall configuration, and threat analysis.", "📞 9800011223", 1),
            ("QA & Automation Test Engineer", "QualityFirst Labs", "Kharadi, Pune", "Pune", "QA Engineer, Automation Test Engineer, Python, Java, SQL", "Graduate", 28000, 48000, "Full-time", "Write automated test suites, execute performance tests, and ensure software release quality.", "📞 9800022334", 1),
            ("Database Administrator & SQL Engineer", "DataVault India", "Nagpur IT Park", "Nagpur", "Database Administrator, Database Engineer, SQL, Data Structures, Excel", "Graduate", 32000, 52000, "Full-time", "Manage database schema migrations, query optimization, backup recovery, and server tuning.", "📞 9800033445", 1),
            ("Embedded Systems & IoT Engineer", "SmartAuto Devices", "MIHAN, Nagpur", "Nagpur", "Embedded Systems Engineer, IoT Engineer, Electronics Engineer, Embedded Systems, IoT, C, C++", "Graduate", 30000, 50000, "Full-time", "Develop micro-controller firmware, sensor networks, and IoT hardware protocols.", "📞 9855044556", 1),
            ("Electrical & PLC Automation Engineer", "Mahindra Industrial Solutions", "Chakan, Pune", "Pune", "Electrical Engineer, Electrical Design, Electronics, PLC, Automation, Quality Control", "Graduate", 32000, 52000, "Full-time", "Design electrical distribution systems, PLC programming, and industrial factory automation.", "📞 9866055667", 1),
            ("Electronics & Hardware Design Engineer", "Circuits India Pvt Ltd", "Satpur MIDC, Nashik", "Nashik", "Electronics Engineer, Electrical Design, Electronics, Manufacturing", "Graduate", 28000, 46000, "Full-time", "PCB layout design, circuit testing, component selection, and hardware debugging.", "📞 9866077889", 1),
            ("Mechanical Design Engineer", "Precision Dynamics", "Ambad MIDC, Nashik", "Nashik", "Mechanical Engineer, Mechanical Design, AutoCAD, SolidWorks, CNC, Manufacturing", "Graduate", 28000, 48000, "Full-time", "3D CAD modeling, component design, SolidWorks simulations, and manufacturing support.", "📞 9877066778", 1),
            ("CNC Manufacturing & Quality Engineer", "AutoPart Tech", "Chhatrapati Sambhajinagar", "Chhatrapati Sambhajinagar", "Mechanical Engineer, CNC, Manufacturing, Quality Control, Mechanical Design", "Graduate", 25000, 42000, "Full-time", "CNC machine programming, quality inspection, precision tolerance testing, and shop floor management.", "📞 9877088990", 1),
            ("Civil Site & Structural Design Engineer", "BuildPro Infra", "Chhatrapati Sambhajinagar", "Chhatrapati Sambhajinagar", "Civil Engineer, Civil Design, Structural Design, Surveying, Site Supervision", "Graduate", 30000, 50000, "Full-time", "Structural calculations, AutoCAD civil drawings, site supervision, and safety auditing.", "📞 9888077889", 1),
            ("Surveying & Site Supervisor", "LandMark Engineering", "Thane West", "Thane", "Civil Engineer, Civil Design, Surveying, Site Supervision", "Graduate", 22000, 38000, "Full-time", "Land measurement, GPS surveying, construction site monitoring, and contractor coordination.", "📞 9888099001", 1),
            ("Robotics & Automation Engineer", "Futura Robotics", "MIDC Jalgaon", "Jalgaon", "Robotics Engineer, Mechatronics, C++, Python, Automation, Electronics", "Graduate", 35000, 60000, "Full-time", "Program robotic arms, vision sensors, and automated guided vehicles for warehouse logistics.", "📞 9811099001", 1),
            ("Chemical Process Engineer", "Biochem Industries", "Roha MIDC, Raigad", "Raigad", "Chemical Engineer, Manufacturing, Quality Control, Process Engineering", "Graduate", 32000, 55000, "Full-time", "Chemical plant operations, safety auditing, process optimization, and quality assurance.", "📞 9811122334", 1),
            ("Biomedical Equipment Engineer", "MedTech Healthcare Systems", "Kolhapur MIDC", "Kolhapur", "Biomedical Engineer, Healthcare, Electronics, Equipment Maintenance", "Graduate", 28000, 45000, "Full-time", "Installation, calibration, and repair of advanced hospital ICU & imaging equipment.", "📞 9822233445", 1),
            ("BI Developer & Data Analyst", "Insight Analytics", "Hinjewadi, Pune", "Pune", "BI Developer, Data Analyst, Business Analyst, SQL, Excel, Power BI, Data Science", "Graduate", 32000, 52000, "Full-time", "Create interactive Power BI dashboards, automated SQL reports, and business analytics.", "📞 9822244556", 1),
        ]
        c.executemany("""INSERT INTO jobs (title,company,location,district,required_skills,min_education,
                         salary_min,salary_max,job_type,description,contact,is_verified) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", jobs)

    c.execute("SELECT COUNT(*) FROM schemes")
    if c.fetchone()[0] == 0:
        schemes = [
            ("PM Awaas Yojana (Urban)","Housing","Free/subsidized housing for urban poor","BPL families in urban slums",60,18,300000,"All","All","₹1.5 Lakh subsidy for home construction or purchase","https://pmaymis.gov.in","Aadhaar, Income proof, Bank account, Photo"),
            ("PM Ujjwala Yojana","Energy","Free LPG connection to BPL families","Women BPL household head",60,18,200000,"Female","All","Free LPG cylinder + stove connection","https://pmuy.gov.in","Aadhaar, BPL card, Bank account"),
            ("Ayushman Bharat (PMJAY)","Health","₹5 Lakh health insurance per family per year","BPL / low income families",100,0,500000,"All","All","₹5 Lakh cashless treatment in empanelled hospitals","https://pmjay.gov.in","Aadhaar, Ration card"),
            ("Skill India / PMKVY","Skill Development","Free vocational training with certification","Unemployed youth",35,15,500000,"All","All","Free training + ₹500/month stipend + job placement","https://pmkvyofficial.org","Aadhaar, 10th mark sheet"),
            ("PM Mudra Yojana","Finance","Loan for small business without collateral","Small/micro business owners",60,18,1000000,"All","All","Loan up to ₹10 Lakh for business","https://mudra.org.in","Aadhaar, Business plan, Bank account"),
            ("Swachh Bharat Mission","Sanitation","Free toilet construction for BPL families","BPL households without toilet",100,18,200000,"All","All","₹12,000 incentive for toilet construction","https://swachhbharat.mygov.in","Aadhaar, BPL card, Photo"),
            ("National Scholarship Portal","Education","Scholarships for SC/ST/OBC students","Students from SC/ST/OBC/minority",25,6,200000,"All","SC,ST,OBC,Minority","₹1,000–₹5,000/month scholarship","https://scholarships.gov.in","School ID, Caste certificate, Bank account"),
            ("Pradhan Mantri Jeevan Jyoti Bima","Insurance","₹2 Lakh life insurance at ₹436/year","All bank account holders",50,18,1000000,"All","All","₹2 Lakh death benefit to nominee","https://jansuraksha.gov.in","Aadhaar, Bank account, Nominee details"),
            ("Rashtriya Parivar Sahayata Yojana","Social Welfare","Financial help to BPL families","BPL family in Maharashtra",65,18,100000,"All","All","₹20,000 one-time financial assistance","https://mahadbt.maharashtra.gov.in","Death certificate, BPL card, Aadhaar"),
            ("Mahatma Gandhi NREGA","Employment","100 days guaranteed wage employment","Rural households",100,18,200000,"All","All","₹200-250/day wage for 100 days","https://nrega.nic.in","Job card, Aadhaar, Bank account"),
        ]
        c.executemany("""INSERT INTO schemes (name,category,description,eligibility,max_age,min_age,max_income,
                         gender,caste,benefits,apply_link,document_required) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", schemes)

    c.execute("SELECT COUNT(*) FROM emergency_contacts")
    if c.fetchone()[0] < 20:
        c.execute("DELETE FROM emergency_contacts")
        contacts = [
            ("iCall - TISS", "Mental Health NGO", "Mumbai", "Mumbai", "9152987821", "TISS Campus, VN Purav Marg, Chembur, Mumbai 400088", "Free mental health counselling, crisis support", "Mon–Sat 8am–10pm"),
            ("Snehi NGO", "Crisis Helpline", "Mumbai", "Mumbai", "044-24640050", "Santacruz East, Mumbai 400055", "Suicide prevention, emotional support helpline", "24/7"),
            ("KEM Hospital", "Government Hospital", "Mumbai", "Mumbai", "022-24136051", "Acharya Donde Marg, Parel, Mumbai 400012", "Emergency, OPD, free treatment for BPL patients", "24/7 Emergency"),
            ("Chhatrapati Shivaji Maharaj Hospital", "Government Hospital", "Thane", "Thane", "022-25345222", "Kalwa Belapur Road, Kalwa, Thane 400605", "24/7 Emergency, General Medicine, Free Ambulance", "24/7 Emergency"),
            ("Sassoon General Hospital", "Government Hospital", "Pune", "Pune", "020-26128000", "Somwar Peth, Near Railway Station, Pune 411001", "Free emergency & OPD services", "24/7 Emergency"),
            ("AIIMS Nagpur", "Government Hospital", "Nagpur", "Nagpur", "0712-2974505", "MIHAN, Nagpur 441108", "Super-specialty medical care, free treatment", "24/7 Emergency"),
            ("District Civil Hospital Nashik", "Government Hospital", "Nashik", "Nashik", "0253-2572038", "Shalimar, Nashik Road, Nashik 422001", "24/7 Free Emergency & Maternity Care", "24/7 Emergency"),
            ("Government Medical College & Hospital (GMC)", "Government Hospital", "Jalgaon", "Jalgaon", "0257-2220982", "Near Prabhat Chowk, Jalgaon 425001", "24/7 Emergency, OPD, ICU, Free Treatment under PMJAY", "24/7 Emergency"),
            ("Civil Hospital Jalgaon", "Government Hospital", "Jalgaon", "Jalgaon", "0257-2226177", "Opp. Collector Office, Jalgaon 425001", "24/7 Trauma Care, Free Ambulance, Maternity Care", "24/7 Emergency"),
            ("Red Cross Society Jalgaon", "Rehabilitation NGO", "Jalgaon", "Jalgaon", "0257-2223700", "Near Railway Station, Jalgaon 425001", "Blood Bank, Emergency Relief, Free Health Camps", "24/7"),
            ("GMCH Sambhajinagar", "Government Hospital", "Chhatrapati Sambhajinagar", "Chhatrapati Sambhajinagar", "0240-2403801", "Panchakki Road, Sambhajinagar 431001", "24/7 Emergency, Surgery, Dialysis, Free OPD", "24/7 Emergency"),
            ("CPR General Hospital", "Government Hospital", "Kolhapur", "Kolhapur", "0231-2654321", "Bhavani Mandap Road, Kolhapur 416002", "24/7 Emergency Trauma & Free Healthcare", "24/7 Emergency"),
            ("Dr. VMS Government Civil Hospital", "Government Hospital", "Solapur", "Solapur", "0217-2744401", "Civil Hospital Chowk, Solapur 413003", "24/7 Emergency & Maternity Services", "24/7 Emergency"),
            ("District General Hospital Amravati", "Government Hospital", "Amravati", "Amravati", "0721-2662201", "Camp Area, Amravati 444602", "24/7 Free OPD, Emergency & Ambulance", "24/7 Emergency"),
            ("Dr. SC Government Medical College", "Government Hospital", "Nanded", "Nanded", "02462-240010", "Vazirabad, Nanded 431601", "24/7 Emergency Medical & Surgical Care", "24/7 Emergency"),
            ("Vasantdada Patil Government Hospital", "Government Hospital", "Sangli", "Sangli", "0233-2374201", "Civil Hospital Road, Sangli 416416", "24/7 Emergency, Blood Bank & Free OPD", "24/7 Emergency"),
            ("Kranti-singha Nana Patil District Hospital", "Government Hospital", "Satara", "Satara", "02162-234501", "Sadar Bazar, Satara 415001", "24/7 Emergency Services & Maternity Wing", "24/7 Emergency"),
            ("Government Medical College & Hospital Latur", "Government Hospital", "Latur", "Latur", "02382-255801", "Gandhi Nagar, Latur 413512", "24/7 Emergency, ICU & Free Treatment", "24/7 Emergency"),
            ("Government Medical College & Hospital Akola", "Government Hospital", "Akola", "Akola", "0724-2434001", "Near Ashok Vatika, Akola 444001", "24/7 Emergency & Free Healthcare Camps", "24/7 Emergency"),
            ("District Civil Hospital Ratnagiri", "Government Hospital", "Ratnagiri", "Ratnagiri", "02352-222301", "Jail Road, Ratnagiri 415612", "24/7 Emergency Trauma & Ambulance", "24/7 Emergency"),
            ("Shri Bhausaheb Hire Government Medical College", "Government Hospital", "Dhule", "Dhule", "02562-239001", "Chakkar Bardi, Dhule 424001", "24/7 Emergency & ICU Services", "24/7 Emergency"),
            ("Government Medical College Chandrapur", "Government Hospital", "Chandrapur", "Chandrapur", "07172-270001", "Ramnagar, Chandrapur 442401", "24/7 Free Emergency & Specialized Care", "24/7 Emergency"),
            ("District Civil Hospital Alibag", "Government Hospital", "Raigad", "Raigad", "02141-222001", "Veshvi, Alibag, Raigad 402201", "24/7 Emergency Healthcare & Free Ambulance", "24/7 Emergency"),
            ("District General Hospital Palghar", "Government Hospital", "Palghar", "Palghar", "02525-252001", "Mahim Road, Palghar 401404", "24/7 Emergency & Tribal Health Assistance", "24/7 Emergency"),
            ("Childline India", "Child Helpline", "All India", "All", "1098", "National helpline", "Child abuse rescue, missing children help", "24/7"),
            ("Women Helpline", "Women Safety", "All India", "All", "181", "National helpline", "Women safety, domestic violence support", "24/7"),
            ("National Emergency", "Police/Fire/Ambulance", "All India", "All", "112", "National helpline", "Police, fire, ambulance emergency", "24/7"),
        ]
        c.executemany("""INSERT INTO emergency_contacts (name,type,location,district,phone,address,services,timing)
                         VALUES (?,?,?,?,?,?,?,?)""", contacts)

    # Free courses seed
    c.execute("SELECT COUNT(*) FROM courses")
    if c.fetchone()[0] == 0:
        courses = [
            ("Electrical Wiring Basics","Electrical","PMKVY / Skill India","Hindi","3 months","Basic electrical wiring, safety, and circuits for home and commercial use","https://pmkvyofficial.org","electrical,wiring,circuits",1),
            ("Mobile Repair Course","Electronics","NIELIT","Hindi/Marathi","2 months","Smartphone hardware & software repair, motherboard basics","https://nielit.gov.in","mobile repair,electronics,hardware",1),
            ("Tailoring & Garment Making","Textile","PMKVY","Hindi","3 months","Basic to advanced stitching, pattern cutting, garment finishing","https://pmkvyofficial.org","stitching,tailoring,sewing",1),
            ("Carpentry & Furniture Making","Construction","Skill India","Hindi","3 months","Wood cutting, furniture making, polishing and finishing","https://skillindia.gov.in","carpentry,furniture,woodwork",1),
            ("Plumbing & Pipe Fitting","Construction","PMKVY","Hindi","2 months","Basic plumbing, pipe fitting, repair and maintenance","https://pmkvyofficial.org","plumbing,pipe fitting,repair",1),
            ("Computer Basics & Data Entry","IT","NIELIT CCC","Hindi/Marathi","3 months","MS Word, Excel, Internet, Email, basic typing skills","https://nielit.gov.in","computer,typing,ms office",1),
            ("Beauty & Wellness","Personal Care","PMKVY","Hindi/Marathi","2 months","Hair, skin, makeup basics — start your own salon","https://pmkvyofficial.org","beauty,salon,makeup",1),
            ("Cooking & Food Processing","Food","PMKVY","Hindi/Marathi","2 months","Professional cooking, food safety, tiffin/catering business","https://pmkvyofficial.org","cooking,food,catering",1),
            ("Two-Wheeler Repair","Automotive","PMKVY","Hindi","3 months","Bike engine, electrical, and repair. Start your own garage.","https://pmkvyofficial.org","driving,vehicle,repair",1),
            ("Security Guard Training","Security","NASSCOM","Hindi","1 month","Physical fitness, first aid, patrolling, emergency response","https://skillindia.gov.in","security,patrolling,vigilance",1),
            ("Painting & Home Decor","Construction","PMKVY","Hindi","2 months","Wall painting, texture, waterproofing for residential work","https://pmkvyofficial.org","painting,wall painting",1),
            ("Digital Literacy","IT","DigiShala / PMGDISHA","Hindi/Marathi","1 month","Smartphone use, UPI payments, internet safety, govt portals","https://pmgdisha.in","computer,mobile,digital",1),
        ]
        c.executemany("""INSERT INTO courses (title,category,provider,language,duration,description,link,skill_tags,is_free)
                         VALUES (?,?,?,?,?,?,?,?,?)""", courses)
