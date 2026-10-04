import streamlit as st
import random
from datetime import datetime, date
from modules.database import get_conn, send_sms
from modules.states_data import get_all_states, get_districts_for_state

EDUCATION_LEVELS = ["No education", "Primary (1-5)", "Middle (6-8)", "8th Pass", "10th Pass", "12th Pass", "ITI/Diploma", "Graduate", "Post Graduate"]
GENDERS = ["Male", "Female", "Other", "Prefer not to say"]
CASTES = ["General", "OBC", "SC", "ST", "NT", "Minority", "Other"]

GRADUATE_DEGREES = [
    "B.E. / B.Tech (Engineering)", "B.Sc (Science)", "B.Com (Commerce)", "B.A. (Arts)", 
    "BCA (Computer Applications)", "BBA (Business Management)", "B.Pharm (Pharmacy)", 
    "MBBS / BDS (Medical)", "LLB (Law)", "B.Arch (Architecture)", "B.Des (Design)", 
    "Other Graduate Degree"
]

PG_DEGREES = [
    "M.E. / M.Tech (Engineering)", "M.Sc (Science)", "M.Com (Commerce)", "M.A. (Arts)", 
    "MCA (Computer Applications)", "MBA (Business Management)", "MD / MS (Medical)", 
    "LLM (Law)", "Ph.D. / Doctorate", "Other Post Graduate Degree"
]

PREDEFINED_SKILLS = [
    # General & Local
    "Driving", "Electrical Work", "Plumbing", "Welding", "Carpentry", "Tailoring", "Stitching", 
    "Cooking", "Construction", "Farming", "Security", "Delivery", "Sales", "Marketing", "Healthcare", "Data Entry",
    
    # Engineering Roles & Skills
    "Mechanical Design", "AutoCAD", "SolidWorks", "CNC", "Manufacturing", "Quality Control", 
    "Electrical Design", "Electronics", "PLC", "Automation", "Embedded Systems", "IoT", 
    "Civil Design", "Structural Design", "Surveying", "Site Supervision",
    "Embedded Systems Engineer", "IoT Engineer", "Electronics Engineer", "Electrical Engineer", 
    "Mechanical Engineer", "Civil Engineer", "Chemical Engineer", "Robotics Engineer", 
    "Biomedical Engineer", "Computer Engineer", "Computer Science Engineer",

    # Computer & IT Roles & Skills
    "Python", "Java", "C", "C++", "JavaScript", "HTML", "CSS", "SQL", "Data Structures", 
    "Data Science", "Machine Learning", "Artificial Intelligence", "Web Development", 
    "App Development", "Cloud Computing", "Cybersecurity", "Networking", "Git/GitHub", "Excel", "Power BI",
    "Data Engineer", "Data Scientist", "Software Engineer", "Software Developer", 
    "Full Stack Developer", "Frontend Developer", "Backend Developer", "Web Developer", 
    "Mobile App Developer", "AI Engineer", "Machine Learning Engineer", "ML Engineer", 
    "DevOps Engineer", "Cloud Engineer", "Cloud Architect", "Cybersecurity Engineer", 
    "Network Engineer", "Database Administrator", "Database Engineer", "BI Developer", 
    "Data Analyst", "Business Analyst", "QA Engineer", "Automation Test Engineer",
    
    # Other
    "Other"
]

def show_login(t):
    st.markdown("""
    <div style="max-width:480px;margin:0 auto;">
    <div class="form-container">
    <div class="form-title">🔐 Login to Your Account</div>
    </div></div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        with st.container():
            st.markdown("""<div style="background:#161b22;border:1px solid #21262d;border-radius:16px;padding:2rem;">""", unsafe_allow_html=True)
            with st.form(key="login_form", clear_on_submit=False):
                phone = st.text_input("📱 Mobile Number", placeholder="Enter 10-digit number", max_chars=10, key="login_phone")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="login_pass")

                if phone and not phone.strip().isdigit():
                    st.error("❌ Mobile number can only contain numbers (0-9).")

                st.markdown("<br>", unsafe_allow_html=True)
                do_login = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")

            if do_login:
                clean_phone = phone.strip()
                if not clean_phone.isdigit() or len(clean_phone) != 10:
                    st.error("❌ Please enter a valid 10-digit mobile number containing only digits.")
                elif phone and password:
                    conn = get_conn()
                    c = conn.cursor()
                    c.execute("SELECT * FROM users WHERE phone=? AND password=?", (clean_phone, password.strip()))
                    user = c.fetchone()
                    conn.close()
                    if user:
                        u_dict = dict(user)
                        if u_dict.get('is_active', 1) == 0:
                            st.error("❌ Account Deactivated: Your account has been suspended by an Admin. Please contact support.")
                        else:
                            st.session_state.user = u_dict
                            if u_dict.get('is_admin'):
                                st.session_state.page = 'admin'
                            else:
                                st.session_state.page = 'jobs'
                            st.success(f"✅ Welcome back, **{user['name']}**!")
                            st.rerun()
                    else:
                        st.error("❌ Invalid mobile number or password.")
                else:
                    st.warning("⚠️ Please enter both fields.")

            st.markdown("<div style='text-align:center;color:#8b949e;font-size:0.85rem;margin-top:1rem;'>Don't have account? Click Register above</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


def show_register(t):
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown("""<div style="background:#161b22;border:1px solid #21262d;border-radius:16px;padding:2rem;">
        <div style="font-family:'Sora',sans-serif;font-size:1.4rem;font-weight:700;color:#e6edf3;margin-bottom:1rem;text-align:center;">
        📝 Create Your Account with SMS OTP Verification</div>""", unsafe_allow_html=True)

        # Initialize Session States for OTP
        if 'otp_sent' not in st.session_state: st.session_state.otp_sent = False
        if 'otp_code' not in st.session_state: st.session_state.otp_code = None
        if 'otp_verified' not in st.session_state: st.session_state.otp_verified = False
        if 'otp_phone' not in st.session_state: st.session_state.otp_phone = ""

        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("👤 Full Name *", placeholder="Enter your full name", key="reg_name")
            email = st.text_input("✉️ Email Address", placeholder="Enter your email address", key="reg_email")
            
            # Mobile Number + Inline Send OTP Button / Verified Badge
            col_p1, col_p2 = st.columns([2.2, 1.1])
            with col_p1:
                phone = st.text_input("📱 Mobile Number *", placeholder="9876543210", max_chars=10, key="reg_phone")
            with col_p2:
                st.markdown("<div style='margin-top:1.75rem;'></div>", unsafe_allow_html=True)
                if st.session_state.otp_verified and st.session_state.otp_phone == phone.strip():
                    st.markdown("""
                    <div style="background:#0d2d1a;border:1px solid #065f46;border-radius:8px;padding:0.45rem 0.5rem;text-align:center;color:#34d399;font-weight:700;font-size:0.82rem;">
                        ✓ Mobile Verified
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    if st.button("📱 Send OTP", use_container_width=True, key="send_otp_btn"):
                        clean_phone = phone.strip()
                        if len(clean_phone) != 10 or not clean_phone.isdigit():
                            st.error("❌ Enter a valid 10-digit mobile number.")
                        else:
                            conn = get_conn()
                            c = conn.cursor()
                            c.execute("SELECT id FROM users WHERE phone=?", (clean_phone,))
                            existing_user = c.fetchone()
                            conn.close()

                            if existing_user:
                                st.error("❌ Number already registered! Click 'Login'.")
                            else:
                                otp = str(random.randint(100000, 999999))
                                st.session_state.otp_code = otp
                                st.session_state.otp_sent = True
                                st.session_state.otp_verified = False
                                st.session_state.otp_phone = clean_phone
                                
                                sms_msg = f"Your Community Hub verification OTP is {otp}"
                                send_sms(clean_phone, sms_msg, sms_type="OTP")
                                st.success("📲 OTP sent!")
            
            # Live validation notice for mobile number
            if phone:
                p_clean = phone.strip()
                if not p_clean.isdigit():
                    st.error("❌ Mobile Number can only contain digits (0-9).")
                elif len(p_clean) < 10:
                    st.caption(f"ℹ️ Mobile number must be 10 digits ({len(p_clean)}/10).")
                elif len(p_clean) == 10:
                    st.caption("✅ Valid 10-digit Mobile Number")
                else:
                    st.error("❌ Mobile number cannot exceed 10 digits.")

            dob_date = st.date_input("📅 Date of Birth (DOB) *", value=None, min_value=date(1940, 1, 1), max_value=date(2012, 12, 31), format="DD/MM/YYYY", key="reg_dob")
            if dob_date:
                dob_str = dob_date.strftime("%d/%m/%Y")
                calc_age = (date.today() - dob_date).days // 365
                st.caption(f"🎂 Calculated Age: **{calc_age} Years**")
            else:
                dob_str = ""
                st.caption("🎂 Select your Date of Birth (Format: DD/MM/YYYY)")

            location = st.text_input("📍 Area / Locality", placeholder="Enter your area or locality", key="reg_location")
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                state_options = ["Select State"] + get_all_states()
                state = st.selectbox("🏛️ State *", state_options, index=0, key="reg_state")
            with col_d2:
                if state == "Select State":
                    district_options = ["Select District"]
                else:
                    district_options = ["Select District"] + get_districts_for_state(state)
                
                district_sel = st.selectbox("🗺️ District *", district_options, index=0, key="reg_district")
                if district_sel in ["Other", "Other District"]:
                    custom_dist = st.text_input("✍️ Enter Your District Name *", placeholder="Type your district name", key="reg_custom_district")
                    district = custom_dist.strip() if custom_dist.strip() else "Other"
                else:
                    district = district_sel

        with col_b:
            gender = st.selectbox("⚥ Gender", GENDERS, key="reg_gender")
            caste = st.selectbox("🏷️ Category", CASTES, key="reg_caste")
            education_level = st.selectbox("🎓 Education Level", EDUCATION_LEVELS, key="reg_edu")
            
            if education_level == "Graduate":
                grad_opts = ["Select Degree / Stream"] + GRADUATE_DEGREES
                degree_sel = st.selectbox("📜 Select Degree / Stream *", grad_opts, index=0, key="reg_grad_deg")
                if degree_sel in ["Select Degree / Stream", ""]:
                    education = "Graduate"
                    degree_valid = False
                elif degree_sel == "Other Graduate Degree":
                    custom_deg = st.text_input("✍️ Enter Your Degree Name *", placeholder="e.g. B.Des, BHM", key="reg_custom_grad_deg")
                    degree_name = custom_deg.strip() if custom_deg.strip() else "Graduate"
                    education = f"Graduate ({degree_name})"
                    degree_valid = True if custom_deg.strip() else False
                else:
                    degree_name = degree_sel.split(' (')[0]
                    education = f"Graduate ({degree_name})"
                    degree_valid = True
            elif education_level == "Post Graduate":
                pg_opts = ["Select Degree / Specialization"] + PG_DEGREES
                degree_sel = st.selectbox("📜 Select Post Graduate Degree / Specialization *", pg_opts, index=0, key="reg_pg_deg")
                if degree_sel in ["Select Degree / Specialization", ""]:
                    education = "Post Graduate"
                    degree_valid = False
                elif degree_sel == "Other Post Graduate Degree":
                    custom_deg = st.text_input("✍️ Enter Your Degree Name *", placeholder="e.g. M.Des, Executive MBA", key="reg_custom_pg_deg")
                    degree_name = custom_deg.strip() if custom_deg.strip() else "Post Graduate"
                    education = f"Post Graduate ({degree_name})"
                    degree_valid = True if custom_deg.strip() else False
                else:
                    degree_name = degree_sel.split(' (')[0]
                    education = f"Post Graduate ({degree_name})"
                    degree_valid = True
            elif education_level == "ITI/Diploma":
                diploma_trade = st.text_input("📜 Trade / Branch (Optional)", placeholder="e.g. Mechanical, Electrician, Civil", key="reg_diploma_trade")
                if diploma_trade.strip():
                    education = f"ITI/Diploma ({diploma_trade.strip()})"
                else:
                    education = "ITI/Diploma"
                degree_valid = True
            else:
                education = education_level
                degree_valid = True
            
            selected_skills = st.multiselect(
                "🧠 Skills (Select Multiple)",
                PREDEFINED_SKILLS,
                placeholder="Choose skills (e.g. Python, AutoCAD, Driving...)",
                key="reg_skills_multi"
            )
            
            custom_skill_text = ""
            if "Other" in selected_skills:
                custom_skill_text = st.text_input("✍️ Enter Custom Skill(s)", placeholder="e.g. Graphic Design, Auto Repair", key="reg_custom_skill")
            
            skills_combined = [s for s in selected_skills if s != "Other"]
            if custom_skill_text.strip():
                skills_combined.append(custom_skill_text.strip())
            skills = ", ".join(skills_combined)

            income = st.number_input("💰 Monthly Income (₹)", min_value=0, max_value=500000, value=0, step=500, key="reg_income")

        password = st.text_input("🔒 Password *", type="password", placeholder="Create a password", key="reg_pass")
        st.markdown("<div style='color:#94a3b8;font-size:0.82rem;margin:-0.3rem 0 0.8rem;'>💡 Minimum 8 characters with uppercase (A-Z), lowercase (a-z), number (0-9), and special character (e.g. Pass@1234).</div>", unsafe_allow_html=True)
        confirm = st.text_input("🔒 Confirm Password *", type="password", placeholder="Repeat password", key="reg_confirm")

        # Step 2: Show Simulated Phone SMS Card for OTP Verification
        if st.session_state.otp_sent and st.session_state.otp_code and not st.session_state.otp_verified:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0d2d1a,#064e3b);border:1px solid #10b981;border-radius:12px;padding:1rem;margin:1rem 0;box-shadow:0 4px 16px rgba(16,185,129,0.2);">
                <div style="display:flex;align-items:center;gap:0.5rem;font-weight:700;color:#34d399;font-size:0.95rem;">
                    📱 SMS received on phone ({st.session_state.otp_phone})
                </div>
                <div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:0.85rem;margin-top:0.6rem;font-family:monospace;font-size:1rem;color:#fde68a;">
                    "Your Community Hub verification OTP is <b style='color:#60a5fa;font-size:1.2rem;'>{st.session_state.otp_code}</b>"
                </div>
            </div>
            """, unsafe_allow_html=True)

            # OTP Input & Verification
            col_v1, col_v2 = st.columns([2, 1])
            with col_v1:
                input_otp = st.text_input("Enter OTP Code", placeholder="e.g. 483921", key="input_otp_code")
            with col_v2:
                st.markdown("<div style='margin-top:1.8rem;'></div>", unsafe_allow_html=True)
                if st.button("Verify OTP", use_container_width=True, key="verify_otp_btn"):
                    if input_otp.strip() == st.session_state.otp_code:
                        st.session_state.otp_verified = True
                        st.success("✅ Mobile Number Verified Successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid OTP. Check the SMS code.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Create Account", use_container_width=True, type="primary", key="do_register"):
            pwd = password.strip()
            conf = confirm.strip()
            clean_email = email.strip()
            
            # Password complexity checks (8+ chars)
            has_upper = any(c.isupper() for c in pwd)
            has_lower = any(c.islower() for c in pwd)
            has_digit = any(c.isdigit() for c in pwd)
            has_special = any(not c.isalnum() for c in pwd)
            
            if not name or not phone or not pwd:
                st.error("❌ Name, Mobile Number and Password are required.")
            elif not dob_date:
                st.error("❌ Please select your Date of Birth (DOB).")
            elif state in ["Select State", ""]:
                st.error("❌ Please select your State.")
            elif district in ["Select District", ""]:
                st.error("❌ Please select your District.")
            elif not degree_valid:
                st.error("❌ Please select or enter your Degree / Stream.")
            elif clean_email and ('@' not in clean_email or '.' not in clean_email):
                st.error("❌ Please enter a valid email address (e.g. name@example.com).")
            elif len(pwd) < 8 or not (has_upper and has_lower and has_digit and has_special):
                st.error("❌ Password does not meet security rules! Must be 8+ characters with uppercase (A-Z), lowercase (a-z), number (0-9), and special character (e.g. Pass@1234).")
            elif pwd != conf:
                st.error("❌ Passwords do not match. Please ensure 'Password' and 'Confirm Password' are identical.")
            elif len(phone.strip()) != 10 or not phone.strip().isdigit():
                st.error("❌ Enter a valid 10-digit mobile number.")
            elif not st.session_state.otp_verified or st.session_state.otp_phone != phone.strip():
                st.error("❌ Please click 'Send OTP' and 'Verify OTP' first before creating account.")
            else:
                try:
                    calc_age = (date.today() - dob_date).days // 365
                    conn = get_conn()
                    c = conn.cursor()
                    c.execute("""INSERT INTO users (name,age,dob,phone,email,password,location,district,state,skills,education,income,gender,caste)
                                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                               (name.strip(), int(calc_age), dob_str, phone.strip(), clean_email, password.strip(),
                                location.strip(), district, state, skills.strip(), education,
                                int(income), gender, caste))
                    conn.commit()
                    uid = c.lastrowid
                    c.execute("SELECT * FROM users WHERE id=?", (uid,))
                    user = c.fetchone()
                    conn.close()

                    # Trigger Registration Confirmation SMS
                    welcome_sms = f"Welcome to Community Hub, {name}! Your account ({phone.strip()}) is verified. You will receive SMS alerts for all job applications & tracking updates."
                    send_sms(phone.strip(), welcome_sms, sms_type="Welcome", user_id=uid)

                    # Reset OTP State
                    st.session_state.otp_sent = False
                    st.session_state.otp_code = None
                    st.session_state.otp_verified = False

                    st.session_state.user = dict(user)
                    st.session_state.page = 'jobs'
                    st.success(f"🎉 Welcome, **{name}**! Account created successfully.")
                    st.rerun()
                except Exception as e:
                    if "UNIQUE" in str(e):
                        st.error("❌ This mobile number is already registered.")
                    else:
                        st.error(f"Error: {e}")

        st.markdown("</div>", unsafe_allow_html=True)
