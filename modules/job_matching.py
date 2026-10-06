import streamlit as st
from modules.database import get_conn
import re

def parse_skills_list(text):
    if not text:
        return []
    raw = [s.strip() for s in re.split(r'[,;\n]+', str(text)) if s.strip()]
    cleaned = []
    seen = set()
    for item in raw:
        c = re.sub(r'\s+', ' ', item).strip()
        if c and c.lower() not in seen:
            seen.add(c.lower())
            cleaned.append(c)
    return cleaned

def is_skill_phrase_match(user_skill, job_skill):
    u = user_skill.lower().strip()
    j = job_skill.lower().strip()
    if u == j or u in j or j in u:
        return True
    u_words = set(re.findall(r'\b[a-z0-9]+\b', u))
    j_words = set(re.findall(r'\b[a-z0-9]+\b', j))
    if u_words and j_words:
        overlap = len(u_words & j_words) / max(len(j_words), len(u_words))
        if overlap >= 0.7:
            return True
    return False

def get_matched_skills_pair(user_skills_str, job_skills_str):
    user_skills = parse_skills_list(user_skills_str)
    job_skills = parse_skills_list(job_skills_str)
    if not job_skills:
        return [], job_skills
    
    matched = []
    for js in job_skills:
        for us in user_skills:
            if is_skill_phrase_match(us, js):
                matched.append(js)
                break
    return matched, job_skills

def skill_match_score(user_skills_str, job_skills_str):
    matched, job_skills = get_matched_skills_pair(user_skills_str, job_skills_str)
    if not job_skills:
        return 0.0
    return min(len(matched) / len(job_skills), 1.0)

def get_matching_skills_explanation(user_skills_str, job_skills_str):
    matched, job_skills = get_matched_skills_pair(user_skills_str, job_skills_str)
    
    if matched:
        matched_list = ", ".join(matched)
        return f"💡 <b>Why this match?</b> Matching skills found in your profile: <span class='why-match-skills'>{matched_list}</span> ({len(matched)} of {len(job_skills)} required skills match)"
    else:
        return "💡 <b>Why this match?</b> General match based on location and background (Update your skills above for a higher AI score)"

def get_job_rating(c, job_id):
    c.execute("SELECT AVG(rating), COUNT(*) FROM job_reviews WHERE job_id=?", (job_id,))
    row = c.fetchone()
    avg = round(row[0], 1) if row[0] else 0.0
    cnt = row[1] or 0
    return avg, cnt

def render_stars(rating):
    full  = int(rating)
    empty = 5 - full
    return "★" * full + "☆" * empty

def show_job_matching(user, t):
    st.markdown(
        "<div class='section-header'>"
        "<div class='section-header-icon'>💼</div>"
        "<div><h2>AI Job Matching</h2>"
        "<p>Skills ke hisab se AI score ke saath best jobs</p></div>"
        "</div>",
        unsafe_allow_html=True
    )

    gender_icon = "👨‍💼" if user.get('gender') == 'Male' else "👩‍💼"
    user_skills_display = user.get('skills', 'None listed')
    
    st.markdown(
        f"""
        <div class='info-box' style='display:flex;align-items:center;gap:1rem;flex-wrap:wrap;'>
            <span style='font-size:2rem;'>{gender_icon}</span>
            <div>
                <div style='font-weight:700;font-size:1.05rem;'>{user['name']}</div>
                <div style='font-size:0.85rem;margin-top:0.25rem;opacity:0.9;'>
                    📍 {user.get('location','N/A')} &nbsp;|&nbsp; 
                    🎓 {user.get('education','N/A')} &nbsp;|&nbsp; 
                    🎯 <b>Preferred Roles / Skills:</b> <span>{user_skills_display}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("🔍 Filter & Search Jobs", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            search = st.text_input("🔎 Keyword", value="", placeholder="Search by job title, skill or keyword", key="job_search")
        with col2:
            all_dists = ["All Districts", "Mumbai", "Thane", "Pune", "Nagpur", "Nashik", "Jalgaon", 
                         "Chhatrapati Sambhajinagar", "Kolhapur", "Solapur", "Amravati", "Nanded", 
                         "Sangli", "Satara", "Latur", "Akola", "Ratnagiri", "Dhule", "Chandrapur", 
                         "Raigad", "Palghar", "Other"]
            user_dist = user.get('district')
            if user_dist and user_dist not in all_dists:
                all_dists.insert(1, user_dist)
            sel_dist = st.selectbox("📍 District", all_dists, key="job_dist")
        with col3:
            sal_ranges = [
                "All Salaries",
                "Below ₹10,000",
                "₹10,000–₹20,000",
                "₹20,000–₹30,000",
                "₹30,000–₹50,000",
                "Above ₹50,000"
            ]
            sel_sal_range = st.selectbox("💰 Salary Range", sal_ranges, key="job_sal_range")

        col4, col5 = st.columns(2)
        with col4:
            job_types = ["All Job Types", "Full Time", "Part Time", "Contract", "Internship", "Work From Home"]
            job_type_sel = st.selectbox("💼 Job Type", job_types, key="job_type_sel")
        with col5:
            sort_options = ["Best Match (AI)", "Nearest", "Highest Salary", "Newest"]
            sort_by = st.selectbox("⚡ Sort By", sort_options, key="job_sort")

        only_verified = st.checkbox("Show Verified Employers Only", value=False, key="job_verified")

    with st.expander("🎤 Apni Skills Update Karo", expanded=False):
        st.markdown(
            "<div style='background:#1a2332;border:1px solid #2d4a8a;border-radius:8px;"
            "padding:0.75rem;color:#94a3b8;font-size:0.85rem;margin-bottom:0.5rem;'>"
            "Mobile Chrome mein keyboard pe microphone icon dabao aur bol do apni skills</div>",
            unsafe_allow_html=True
        )
        manual_skills = st.text_area("Skills type karo:", placeholder="electrical, driving, stitching...",
                                      key="manual_skills", height=60)
        if st.button("Save Skills", key="save_skills"):
            if manual_skills.strip():
                conn2 = get_conn()
                conn2.execute("UPDATE users SET skills=? WHERE id=?", (manual_skills.strip(), user['id']))
                conn2.commit()
                conn2.close()
                user['skills'] = manual_skills.strip()
                st.success("Skills update ho gayi!")
                st.rerun()

    conn = get_conn()
    c    = conn.cursor()

    query  = "SELECT * FROM jobs WHERE is_active=1"
    params = []
    if sel_dist != "All Districts":
        query += " AND district=?"
        params.append(sel_dist)
    if job_type_sel != "All Job Types":
        jt_clean = job_type_sel.replace(" ", "-")
        query += " AND (job_type=? OR job_type=?)"
        params.extend([job_type_sel, jt_clean])
    if only_verified:
        query += " AND is_verified=1"
    if search.strip():
        query += " AND (title LIKE ? OR required_skills LIKE ? OR description LIKE ? OR company LIKE ?)"
        params.extend(["%" + search.strip() + "%"] * 4)

    c.execute(query, params)
    jobs = [dict(r) for r in c.fetchall()]

    # Salary Range filtering
    if sel_sal_range == "Below ₹10,000":
        jobs = [j for j in jobs if j.get('salary_min', 0) < 10000]
    elif sel_sal_range == "₹10,000–₹20,000":
        jobs = [j for j in jobs if (j.get('salary_max', 0) >= 10000 and j.get('salary_min', 0) <= 20000)]
    elif sel_sal_range == "₹20,000–₹30,000":
        jobs = [j for j in jobs if (j.get('salary_max', 0) >= 20000 and j.get('salary_min', 0) <= 30000)]
    elif sel_sal_range == "₹30,000–₹50,000":
        jobs = [j for j in jobs if (j.get('salary_max', 0) >= 30000 and j.get('salary_min', 0) <= 50000)]
    elif sel_sal_range == "Above ₹50,000":
        jobs = [j for j in jobs if (j.get('salary_max', 0) >= 50000 or j.get('salary_min', 0) >= 50000)]

    user_skills = user.get('skills', '')
    user_dist_name = (user.get('district') or '').strip().lower()

    for job in jobs:
        job['_score'] = skill_match_score(user_skills, job['required_skills'])
        job['_avg_rating'], job['_rating_count'] = get_job_rating(c, job['id'])
        job['_is_nearest'] = (job.get('district', '').strip().lower() == user_dist_name)

    # Sorting
    if sort_by == "Best Match (AI)":
        jobs.sort(key=lambda x: x['_score'], reverse=True)
    elif sort_by == "Nearest":
        jobs.sort(key=lambda x: (x['_is_nearest'], x['_score']), reverse=True)
    elif sort_by == "Highest Salary":
        jobs.sort(key=lambda x: x.get('salary_max', 0), reverse=True)
    elif sort_by == "Newest":
        jobs.sort(key=lambda x: x.get('id', 0), reverse=True)

    c.execute("SELECT job_id FROM applications WHERE user_id=?", (user['id'],))
    applied_ids = set(r['job_id'] for r in c.fetchall())

    st.markdown(
        "<div style='color:#8b949e;font-size:0.85rem;margin-bottom:1rem;'>"
        "Showing <b style='color:#60a5fa;font-size:1rem;'>" + str(len(jobs)) + "</b> matching jobs</div>",
        unsafe_allow_html=True
    )

    if not jobs:
        st.markdown(
            "<div style='text-align:center;padding:3rem;color:#8b949e;'>"
            "<div style='font-size:3rem;margin-bottom:1rem;'>🔍</div>"
            "<div>Koi job nahi mili. Filters badal kar dekhein.</div></div>",
            unsafe_allow_html=True
        )
        conn.close()
        return

    for job in jobs:
        score_pct  = int(job['_score'] * 100)
        bar_color  = "#34d399" if score_pct >= 70 else "#f59e0b" if score_pct >= 40 else "#6b7280"
        avg_rating = job['_avg_rating']
        rating_cnt = job['_rating_count']
        stars_str  = render_stars(avg_rating)
        applied    = job['id'] in applied_ids

        verified_badge = ""
        if job.get('is_verified'):
            verified_badge = (
                " <span style='background:#0d2d1a;color:#34d399;border:1px solid #065f46;"
                "border-radius:6px;padding:2px 8px;font-size:0.75rem;font-weight:600;'>✔ Verified</span>"
            )

        skills_pills = "".join([f"<span class='badge badge-purple' style='font-size:0.78rem;margin:2px 4px 2px 0;display:inline-block;'>{s.strip()}</span>" for s in job['required_skills'].split(',') if s.strip()])
        why_match_html = get_matching_skills_explanation(user_skills, job['required_skills'])

        card_html = (
            "<div class='job-card' style='position:relative;'>"
            "<div style='display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.5rem;'>"
            "<div>"
            f"<div class='job-title'>{job['title']}</div>"
            f"<div class='job-company' style='margin-top:0.25rem;display:flex;align-items:center;gap:0.4rem;flex-wrap:wrap;'>🏢 {job['company']} {verified_badge}</div>"
            "</div>"
            f"<div class='match-score' style='position:static;'>🤖 {score_pct}% Match</div>"
            "</div>"
            "<div style='display:flex;flex-wrap:wrap;gap:0.5rem;margin:0.75rem 0;'>"
            f"<span class='badge badge-blue' style='font-size:0.8rem;'>📍 {job['location']}</span>"
            f"<span class='badge badge-green' style='font-size:0.8rem;'>💰 ₹{job['salary_min']:,}–₹{job['salary_max']:,}/mo</span>"
            f"<span class='badge badge-purple' style='font-size:0.8rem;'>🕐 {job['job_type']}</span>"
            f"<span class='badge badge-orange' style='font-size:0.8rem;'>🎓 {job['min_education']}</span>"
            "</div>"
            f"<div class='job-desc'>{job['description']}</div>"
            f"<div style='margin-bottom:0.6rem;'><span class='stat-label'>🔧 Required Skills: </span>{skills_pills}</div>"
            f"<div class='job-why-match'>{why_match_html}</div>"
            f"<div class='match-bar-container' style='margin-top:0.6rem;'><div class='match-bar' style='width:{score_pct}%;background:{bar_color};'></div></div>"
            "<div style='display:flex;align-items:center;justify-content:space-between;margin-top:0.6rem;padding-top:0.6rem;border-top:1px solid rgba(128,128,128,0.2);'>"
            f"<div style='display:flex;align-items:center;gap:0.5rem;'><span style='color:#f59e0b;font-size:0.9rem;'>{stars_str}</span><span class='stat-label'>{avg_rating}/5 ({rating_cnt} reviews)</span></div>"
            f"<div class='job-company' style='font-weight:600;font-size:0.82rem;'>📞 {job['contact']}</div>"
            "</div>"
            "</div>"
        )
        st.markdown(card_html, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            if applied:
                st.markdown(
                    "<div class='success-box' style='padding:0.45rem 0.8rem;text-align:center;font-size:0.85rem;'>✅ Applied</div>",
                    unsafe_allow_html=True
                )
            else:
                if st.button("Apply Now", key="apply_" + str(job['id']), use_container_width=True):
                    conn.execute("INSERT INTO applications (user_id,job_id) VALUES (?,?)", (user['id'], job['id']))
                    conn.commit()
                    applied_ids.add(job['id'])
                    
                    # Trigger SMS Notification
                    from modules.database import send_sms
                    job_sms = f"📱 Smart Slum Job Alert: Your application for '{job['title']}' at '{job['company']}' has been submitted! Status: Applied."
                    send_sms(user['phone'], job_sms, sms_type="Job Application", user_id=user['id'])
                    st.toast("📱 SMS Alert sent to your phone!", icon="💬")

                    st.success("Application submit ho gayi!")
                    st.rerun()
        with col2:
            if st.button("Rate & Review", key="rate_" + str(job['id']), use_container_width=True):
                if 'review_job' not in st.session_state or st.session_state['review_job'] != job['id']:
                    st.session_state['review_job'] = job['id']
                else:
                    st.session_state.pop('review_job', None)
                st.rerun()

        if st.session_state.get('review_job') == job['id']:
            st.markdown(
                "<div style='background:#1a2332;border:1px solid #2d4a8a;border-radius:10px;padding:1rem;margin-bottom:0.5rem;'>",
                unsafe_allow_html=True
            )
            c.execute("SELECT * FROM job_reviews WHERE user_id=? AND job_id=?", (user['id'], job['id']))
            existing = c.fetchone()
            existing = dict(existing) if existing else None

            r_rating = st.slider("Rating", 1, 5, int(existing['rating']) if existing else 4,
                                  key="r_slider_" + str(job['id']))
            stars_preview = "★" * r_rating + "☆" * (5 - r_rating)
            st.markdown("<span style='color:#f59e0b;font-size:1.2rem;'>" + stars_preview + "</span>", unsafe_allow_html=True)
            r_text = st.text_area("Review (optional)", value=existing['review'] if existing else '',
                                   placeholder="Company kaisi hai? Salary time pe milti hai?",
                                   height=70, key="r_text_" + str(job['id']))
            rc1, rc2 = st.columns(2)
            with rc1:
                if st.button("Submit Review", key="sub_rev_" + str(job['id'])):
                    if existing:
                        conn.execute("UPDATE job_reviews SET rating=?,review=? WHERE id=?",
                                     (r_rating, r_text, existing['id']))
                    else:
                        conn.execute("INSERT INTO job_reviews (user_id,job_id,rating,review) VALUES (?,?,?,?)",
                                     (user['id'], job['id'], r_rating, r_text))
                    conn.commit()
                    st.session_state.pop('review_job', None)
                    st.success("Review submit ho gayi!")
                    st.rerun()
            with rc2:
                if st.button("Cancel", key="cancel_" + str(job['id'])):
                    st.session_state.pop('review_job', None)
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    conn.close()

