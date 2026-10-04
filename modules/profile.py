import streamlit as st
import re
import pandas as pd
from modules.database import get_conn
from modules.job_matching import skill_match_score, render_stars, get_job_rating
from modules.states_data import get_all_states, get_districts_for_state
from modules.auth import PREDEFINED_SKILLS, GRADUATE_DEGREES, PG_DEGREES

EDUCATION_LEVELS = ["No education", "Primary (1-5)", "Middle (6-8)", "8th Pass", "10th Pass", "12th Pass", "ITI/Diploma", "Graduate", "Post Graduate"]
GENDERS = ["Male", "Female", "Other"]
CASTES = ["General", "OBC", "SC", "ST", "NT", "Minority", "Other"]

def calculate_profile_completion(user):
    fields = [
        user.get('name'),
        user.get('phone'),
        user.get('age'),
        user.get('gender'),
        user.get('district'),
        user.get('location'),
        user.get('education'),
        user.get('skills'),
        user.get('income'),
        user.get('caste')
    ]
    filled = sum(1 for f in fields if f is not None and str(f).strip() != '' and str(f) != '0')
    return int((filled / len(fields)) * 100)

def show_user_profile(user, t):
    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon">👤</div>
        <div>
            <h2>Personal User Dashboard</h2>
            <p>Manage your profile, skills, job applications, and personalized recommendations</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    completion_score = calculate_profile_completion(user)
    gender_icon = "👨‍💼" if user.get('gender') == 'Male' else "👩‍💼"

    # Profile Summary Banner & Completion Meter
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #1a2744 0%, #0d1b3e 100%);border:1px solid #2d4a8a;border-radius:16px;padding:1.5rem;margin-bottom:1.5rem;box-shadow:0 4px 24px rgba(59,130,246,0.15);">
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
            <div style="display:flex;align-items:center;gap:1rem;">
                <div style="font-size:3rem;background:#161b22;border:1px solid #30363d;border-radius:50%;width:70px;height:70px;display:flex;align-items:center;justify-content:center;">
                    {gender_icon}
                </div>
                <div>
                    <div style="font-family:'Sora',sans-serif;font-size:1.3rem;font-weight:700;color:#ffffff;">
                        {user.get('name', 'User')}
                        <span style="background:#0d2d1a;color:#34d399;border:1px solid #065f46;border-radius:6px;padding:2px 8px;font-size:0.75rem;margin-left:0.5rem;">
                            ✅ Mobile Verified ({user.get('phone')})
                        </span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.88rem;margin-top:0.2rem;">
                        📍 {user.get('location','N/A')}, {user.get('district','N/A')} &nbsp;|&nbsp; 🎓 {user.get('education','N/A')} &nbsp;|&nbsp; 💰 ₹{user.get('income',0)}/mo
                    </div>
                </div>
            </div>
            <div style="min-width:180px;text-align:right;">
                <div style="color:#60a5fa;font-size:0.85rem;font-weight:600;margin-bottom:4px;">
                    Profile Completion: {completion_score}%
                </div>
                <div style="background:#21262d;border-radius:6px;height:8px;overflow:hidden;width:180px;display:inline-block;">
                    <div style="width:{completion_score}%;height:100%;background:linear-gradient(90deg, #3b82f6, #34d399);border-radius:6px;"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Dashboard Tabs
    tabs = st.tabs([
        "👤 My Profile", 
        "✏️ Edit Profile", 
        "🛠️ My Skills", 
        "💼 My Applications", 
        "🎯 Recommended Jobs", 
        "🎓 Recommended Courses", 
        "🏛️ Recommended Schemes", 
        "🔐 Change Password"
    ])

    # ══════════════════════════════════════════════════════════════════
    # TAB 1 — MY PROFILE
    # ══════════════════════════════════════════════════════════════════
    with tabs[0]:
        st.markdown("### Profile Summary")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown(f"""
            <div style="background:#161b22;border:1px solid #21262d;border-radius:12px;padding:1.2rem;margin-bottom:1rem;">
                <div style="color:#8b949e;font-size:0.8rem;margin-bottom:0.2rem;">FULL NAME</div>
                <div style="color:#e6edf3;font-size:1rem;font-weight:600;">{user.get('name')}</div>
                <hr style="border-color:#21262d;margin:0.8rem 0;">
                <div style="color:#8b949e;font-size:0.8rem;margin-bottom:0.2rem;">MOBILE NUMBER</div>
                <div style="color:#60a5fa;font-size:1rem;font-weight:600;">📱 {user.get('phone')} <span style="color:#34d399;font-size:0.8rem;">(Verified)</span></div>
                <hr style="border-color:#21262d;margin:0.8rem 0;">
                <div style="color:#8b949e;font-size:0.8rem;margin-bottom:0.2rem;">EMAIL ADDRESS</div>
                <div style="color:#e6edf3;font-size:1rem;font-weight:600;">✉️ {user.get('email') if user.get('email') else 'Not provided'}</div>
                <hr style="border-color:#21262d;margin:0.8rem 0;">
                <div style="color:#8b949e;font-size:0.8rem;margin-bottom:0.2rem;">AGE & GENDER</div>
                <div style="color:#e6edf3;font-size:1rem;font-weight:600;">{user.get('age')} Years &nbsp;•&nbsp; {user.get('gender')}</div>
                <hr style="border-color:#21262d;margin:0.8rem 0;">
                <div style="color:#8b949e;font-size:0.8rem;margin-bottom:0.2rem;">CATEGORY / CASTE</div>
                <div style="color:#e6edf3;font-size:1rem;font-weight:600;">{user.get('caste', 'General')}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_p2:
            st.markdown(f"""
            <div style="background:#161b22;border:1px solid #21262d;border-radius:12px;padding:1.2rem;margin-bottom:1rem;">
                <div style="color:#8b949e;font-size:0.8rem;margin-bottom:0.2rem;">LOCATION & DISTRICT</div>
                <div style="color:#e6edf3;font-size:1rem;font-weight:600;">📍 {user.get('location')}, {user.get('district')}</div>
                <hr style="border-color:#21262d;margin:0.8rem 0;">
                <div style="color:#8b949e;font-size:0.8rem;margin-bottom:0.2rem;">EDUCATION LEVEL</div>
                <div style="color:#e6edf3;font-size:1rem;font-weight:600;">🎓 {user.get('education')}</div>
                <hr style="border-color:#21262d;margin:0.8rem 0;">
                <div style="color:#8b949e;font-size:0.8rem;margin-bottom:0.2rem;">MONTHLY INCOME</div>
                <div style="color:#34d399;font-size:1rem;font-weight:600;">💰 ₹{user.get('income', 0)} / month</div>
                <hr style="border-color:#21262d;margin:0.8rem 0;">
                <div style="color:#8b949e;font-size:0.8rem;margin-bottom:0.2rem;">SKILLS</div>
                <div style="color:#60a5fa;font-size:1rem;font-weight:600;">🧠 {user.get('skills', 'No skills listed')}</div>
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # TAB 2 — EDIT PROFILE
    # ══════════════════════════════════════════════════════════════════
    with tabs[1]:
        st.markdown("""
        <style>
        div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] > button {
            background-color: #2563EB !important;
            background: #2563EB !important;
            border-color: #2563EB !important;
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] > button:hover {
            background-color: #1D4ED8 !important;
            background: #1D4ED8 !important;
            border-color: #1D4ED8 !important;
            color: #ffffff !important;
            box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("### Update Your Personal Information")
        with st.form("edit_profile_form"):
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                e_name = st.text_input("Full Name", value=user.get('name',''))
                e_email = st.text_input("Email Address", value=user.get('email',''))
                e_age = st.number_input("Age", min_value=14, max_value=80, value=int(user.get('age',25)))
                e_location = st.text_input("Area / Locality", value=user.get('location',''))
                
                all_states = get_all_states()
                cur_state = user.get('state', 'Maharashtra')
                st_idx = all_states.index(cur_state) if cur_state in all_states else 0
                e_state = st.selectbox("State", all_states, index=st_idx, key="edit_state")
                
                state_districts = get_districts_for_state(e_state)
                cur_dist = user.get('district', '')
                dt_idx = state_districts.index(cur_dist) if cur_dist in state_districts else (state_districts.index("Other") if "Other" in state_districts else 0)
                e_district_sel = st.selectbox("District", state_districts, index=dt_idx, key="edit_district")
                if e_district_sel in ["Other", "Other District"]:
                    e_custom_dist = st.text_input("✍️ Enter Your District Name", value=cur_dist if cur_dist not in state_districts else "", placeholder="Type your district name", key="edit_custom_district")
                    e_district = e_custom_dist.strip() if e_custom_dist.strip() else "Other"
                else:
                    e_district = e_district_sel
            with col_e2:
                e_gender = st.selectbox("Gender", GENDERS, index=GENDERS.index(user.get('gender')) if user.get('gender') in GENDERS else 0)
                e_caste = st.selectbox("Category / Caste", CASTES, index=CASTES.index(user.get('caste')) if user.get('caste') in CASTES else 0)
                
                cur_edu_raw = user.get('education', 'No education')
                cur_edu_level = cur_edu_raw.split(' (')[0] if '(' in cur_edu_raw else cur_edu_raw
                edu_idx = EDUCATION_LEVELS.index(cur_edu_level) if cur_edu_level in EDUCATION_LEVELS else 0
                e_edu_level = st.selectbox("Education Level", EDUCATION_LEVELS, index=edu_idx, key="edit_edu_level")

                if e_edu_level == "Graduate":
                    e_deg_sel = st.selectbox("Graduate Degree / Stream", GRADUATE_DEGREES, key="edit_grad_deg")
                    if e_deg_sel == "Other Graduate Degree":
                        e_custom_deg = st.text_input("✍️ Degree Name", value="", key="edit_custom_grad_deg")
                        e_deg_name = e_custom_deg.strip() if e_custom_deg.strip() else "Graduate"
                    else:
                        e_deg_name = e_deg_sel.split(' (')[0]
                    e_edu = f"Graduate ({e_deg_name})"
                elif e_edu_level == "Post Graduate":
                    e_deg_sel = st.selectbox("Post Graduate Degree / Specialization", PG_DEGREES, key="edit_pg_deg")
                    if e_deg_sel == "Other Post Graduate Degree":
                        e_custom_deg = st.text_input("✍️ Degree Name", value="", key="edit_custom_pg_deg")
                        e_deg_name = e_custom_deg.strip() if e_custom_deg.strip() else "Post Graduate"
                    else:
                        e_deg_name = e_deg_sel.split(' (')[0]
                    e_edu = f"Post Graduate ({e_deg_name})"
                elif e_edu_level == "ITI/Diploma":
                    e_trade = st.text_input("Trade / Branch (Optional)", value="", key="edit_diploma_trade")
                    e_edu = f"ITI/Diploma ({e_trade.strip()})" if e_trade.strip() else "ITI/Diploma"
                else:
                    e_edu = e_edu_level

                e_income = st.number_input("Monthly Income (₹)", min_value=0, max_value=500000, value=int(user.get('income',0)), step=500)

            st.markdown("<br>", unsafe_allow_html=True)
            submit_profile = st.form_submit_button("💾 Save Profile Changes", use_container_width=True, type="primary")

            if submit_profile:
                if not e_name.strip():
                    st.error("❌ Full Name cannot be empty.")
                else:
                    conn = get_conn()
                    conn.execute("""
                        UPDATE users SET name=?, email=?, age=?, location=?, state=?, district=?, gender=?, caste=?, education=?, income=?
                        WHERE id=?
                    """, (e_name.strip(), e_email.strip(), int(e_age), e_location.strip(), e_state, e_district, e_gender, e_caste, e_edu, int(e_income), user['id']))
                    conn.commit()
                    
                    # Sync session state
                    c = conn.cursor()
                    c.execute("SELECT * FROM users WHERE id=?", (user['id'],))
                    updated_user = c.fetchone()
                    conn.close()
                    
                    st.session_state.user = dict(updated_user)
                    st.success("✅ Profile updated successfully!")
                    st.rerun()

    # ══════════════════════════════════════════════════════════════════
    # TAB 3 — MY SKILLS MANAGER
    # ══════════════════════════════════════════════════════════════════
    with tabs[2]:
        st.markdown("### 🧠 Skills & Experience Manager")
        st.markdown("<div style='color:#8b949e;font-size:0.88rem;margin-bottom:1rem;'>Updating your skills will automatically update your AI Job Matching score in real-time!</div>", unsafe_allow_html=True)

        current_skills_raw = user.get('skills', '')
        skills_list = [s.strip() for s in current_skills_raw.split(',') if s.strip()]

        st.markdown("##### Current Skills Tags:")
        if skills_list:
            tags_html = " ".join([f"<span class='badge badge-blue' style='font-size:0.9rem;padding:0.4rem 0.8rem;margin:0.2rem;'>✨ {s}</span>" for s in skills_list])
            st.markdown(f"<div style='margin-bottom:1rem;'>{tags_html}</div>", unsafe_allow_html=True)
        else:
            st.warning("No skills added yet.")

        st.markdown("<hr style='border-color:#21262d;'>", unsafe_allow_html=True)
        
        with st.form("update_skills_form"):
            existing_predefined = [s for s in skills_list if s in PREDEFINED_SKILLS and s != "Other"]
            existing_custom = [s for s in skills_list if s not in PREDEFINED_SKILLS]
            
            p_selected = st.multiselect("Select Skills from List", [s for s in PREDEFINED_SKILLS if s != "Other"], default=existing_predefined, key="prof_multi_skills")
            p_custom = st.text_input("Other Custom Skills (comma separated)", value=", ".join(existing_custom), placeholder="e.g. Graphic Design, Auto Repair", key="prof_custom_skills")
            
            submit_skills = st.form_submit_button("⚡ Update Skills & Sync AI Job Matcher", use_container_width=True, type="primary")

            if submit_skills:
                combined_p_skills = list(p_selected)
                if p_custom.strip():
                    for cs in p_custom.split(','):
                        if cs.strip(): combined_p_skills.append(cs.strip())
                new_skills_str = ", ".join(combined_p_skills)

                conn = get_conn()
                conn.execute("UPDATE users SET skills=? WHERE id=?", (new_skills_str, user['id']))
                conn.commit()
                
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE id=?", (user['id'],))
                updated_user = c.fetchone()
                conn.close()

                st.session_state.user = dict(updated_user)
                st.success("🎉 Skills updated! Your job recommendations have been updated.")
                st.rerun()

    # ══════════════════════════════════════════════════════════════════
    # TAB 4 — MY APPLICATIONS
    # ══════════════════════════════════════════════════════════════════
    with tabs[3]:
        st.markdown("### 💼 Your Applied Jobs")
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            SELECT a.id, j.title, j.company, j.location, j.salary_min, j.salary_max,
                   a.status, a.applied_at, a.notes, j.contact
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            WHERE a.user_id = ?
            ORDER BY a.applied_at DESC
        """, (user['id'],))
        apps = [dict(r) for r in c.fetchall()]
        conn.close()

        if not apps:
            st.info("You haven't applied for any jobs yet. Go to 'Recommended Jobs' or 'Jobs' page to apply!")
        else:
            for app in apps:
                applied_date = app['applied_at'][:10] if app['applied_at'] else "N/A"
                st.markdown(f"""
                <div class="job-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div style="font-family:'Sora',sans-serif;font-weight:600;font-size:1.05rem;color:#e6edf3;">{app['title']}</div>
                        <span class="badge badge-purple" style="font-size:0.82rem;">{app['status']}</span>
                    </div>
                    <div style="color:#60a5fa;font-size:0.9rem;margin-top:0.2rem;">🏢 {app['company']}</div>
                    <div class="job-meta" style="margin:0.5rem 0;">
                        <span class="badge badge-blue">📍 {app['location']}</span>
                        <span class="badge badge-green">💰 ₹{app['salary_min']}–₹{app['salary_max']}/mo</span>
                        <span class="badge badge-orange">📅 Applied: {applied_date}</span>
                    </div>
                    <div style="color:#8b949e;font-size:0.82rem;margin-top:0.3rem;">📞 Contact: {app['contact']}</div>
                </div>
                """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # TAB 5 — RECOMMENDED JOBS (AI MATCH)
    # ══════════════════════════════════════════════════════════════════
    with tabs[4]:
        st.markdown("### 🎯 AI Recommended Jobs For You")
        user_skills = user.get('skills', '')
        
        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT * FROM jobs WHERE is_active=1")
        all_jobs = [dict(r) for r in c.fetchall()]
        
        c.execute("SELECT job_id FROM applications WHERE user_id=?", (user['id'],))
        applied_job_ids = set(r[0] for r in c.fetchall())
        conn.close()

        # Score jobs
        scored_jobs = []
        for j in all_jobs:
            score = skill_match_score(user_skills, j.get('required_skills', ''))
            scored_jobs.append((score, j))
        
        scored_jobs.sort(key=lambda x: x[0], reverse=True)

        for score, job in scored_jobs[:6]:
            score_pct = int(score * 100)
            applied = job['id'] in applied_job_ids
            
            st.markdown(f"""
            <div class="job-card">
                <div class="match-score">🤖 {score_pct}% match</div>
                <div class="job-title">{job['title']}</div>
                <div class="job-company">🏢 {job['company']}</div>
                <div class="job-meta">
                    <span class="badge badge-blue">📍 {job['location']}</span>
                    <span class="badge badge-green">💰 ₹{job['salary_min']}–₹{job['salary_max']}/mo</span>
                    <span class="badge badge-purple">🕐 {job['job_type']}</span>
                </div>
                <div style="color:#94a3b8;font-size:0.85rem;margin:0.4rem 0;">{job['description']}</div>
                <div style="color:#8b949e;font-size:0.82rem;">Required Skills: <span style="color:#60a5fa;">{job['required_skills']}</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            if applied:
                st.markdown("<div class='success-box' style='padding:0.3rem;text-align:center;font-size:0.82rem;'>✅ Applied</div>", unsafe_allow_html=True)
            else:
                if st.button("Apply Now", key=f"rec_apply_{job['id']}", use_container_width=True):
                    conn = get_conn()
                    conn.execute("INSERT INTO applications (user_id, job_id) VALUES (?,?)", (user['id'], job['id']))
                    conn.commit()
                    conn.close()
                    st.success(f"Applied for {job['title']}!")
                    st.rerun()

    # ══════════════════════════════════════════════════════════════════
    # TAB 6 — RECOMMENDED COURSES
    # ══════════════════════════════════════════════════════════════════
    with tabs[5]:
        st.markdown("### 🎓 Recommended Free Skill Courses")
        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT * FROM courses WHERE is_free=1")
        all_courses = [dict(r) for r in c.fetchall()]
        conn.close()

        for crs in all_courses[:6]:
            st.markdown(f"""
            <div class="feature-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <h3>🎓 {crs['title']}</h3>
                    <span class="badge badge-green">FREE</span>
                </div>
                <div style="color:#60a5fa;font-size:0.85rem;margin:0.3rem 0;">🏛️ Provider: {crs['provider']} &nbsp;|&nbsp; ⏱️ Duration: {crs['duration']}</div>
                <p style="color:#94a3b8;font-size:0.85rem;">{crs['description']}</p>
                <div style="margin-top:0.6rem;">
                    <a href="{crs['link']}" target="_blank" style="text-decoration:none;">
                        <span style="background:#1e3a5f;color:#60a5fa;border:1px solid #2d4a8a;padding:0.3rem 0.75rem;border-radius:6px;font-size:0.8rem;font-weight:600;">
                            🚀 Enroll Free
                        </span>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # TAB 7 — RECOMMENDED SCHEMES
    # ══════════════════════════════════════════════════════════════════
    with tabs[6]:
        st.markdown("### 🏛️ Government Schemes You Are Eligible For")
        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT * FROM schemes")
        all_schemes = [dict(r) for r in c.fetchall()]
        conn.close()

        user_age = int(user.get('age', 25))
        user_inc = int(user.get('income', 0)) * 12 # Annual income

        eligible_schemes = []
        for sch in all_schemes:
            max_a = sch.get('max_age', 100) or 100
            min_a = sch.get('min_age', 0) or 0
            max_i = sch.get('max_income', 10000000) or 10000000
            
            if min_a <= user_age <= max_a and user_inc <= max_i:
                eligible_schemes.append(sch)

        for sch in eligible_schemes[:6]:
            st.markdown(f"""
            <div class="scheme-card">
                <div class="scheme-title">🏛️ {sch['name']}</div>
                <div class="scheme-benefit">✨ Benefit: {sch['benefits']}</div>
                <p style="color:#94a3b8;font-size:0.85rem;">{sch['description']}</p>
                <div style="color:#8b949e;font-size:0.8rem;margin-top:0.4rem;">📄 Documents Required: {sch['document_required']}</div>
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # TAB 8 — CHANGE PASSWORD
    # ══════════════════════════════════════════════════════════════════
    with tabs[7]:
        st.markdown("### 🔐 Security & Change Password")
        with st.form("change_pass_form"):
            curr_pass = st.text_input("Current Password", type="password", key="cp_curr")
            new_pass = st.text_input("New Password", type="password", key="cp_new")
            st.markdown("<div style='color:#94a3b8;font-size:0.82rem;margin:-0.3rem 0 0.8rem;'>💡 Use 6+ characters with uppercase, lowercase, numbers, and special characters.</div>", unsafe_allow_html=True)
            conf_pass = st.text_input("Confirm New Password", type="password", key="cp_conf")
            
            submit_pass = st.form_submit_button("🔒 Change Password", use_container_width=True, type="primary")

            if submit_pass:
                pwd = new_pass.strip()
                conf = conf_pass.strip()
                
                has_upper = any(c.isupper() for c in pwd)
                has_lower = any(c.islower() for c in pwd)
                has_digit = any(c.isdigit() for c in pwd)
                has_special = any(not c.isalnum() for c in pwd)

                if curr_pass.strip() != user.get('password'):
                    st.error("❌ Incorrect current password.")
                elif len(pwd) < 6 or not (has_upper and has_lower and has_digit and has_special):
                    st.error("❌ New password does not meet security rules! Must be 6+ characters with uppercase, lowercase, number, and special character.")
                elif pwd != conf:
                    st.error("❌ New password and confirmation do not match.")
                else:
                    conn = get_conn()
                    conn.execute("UPDATE users SET password=? WHERE id=?", (pwd, user['id']))
                    conn.commit()
                    conn.close()
                    user['password'] = pwd
                    st.success("🎉 Password updated successfully!")
                    st.rerun()


