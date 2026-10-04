import streamlit as st
import re
from modules.database import get_conn

def parse_skill_phrases(text):
    """
    Parses comma/semicolon/newline-separated skills into clean phrases.
    Preserves multi-word roles like 'Data Engineer', 'Data Scientist', 'Full Stack Developer'.
    """
    if not text:
        return []
    raw = [s.strip() for s in re.split(r'[,;\n]+', str(text)) if s.strip()]
    result = []
    seen = set()
    for item in raw:
        clean = re.sub(r'\s+', ' ', item).strip()
        if clean and clean.lower() not in seen:
            seen.add(clean.lower())
            result.append(clean)
    return result


def is_skill_matched(user_skill_phrase, job_skill_phrase):
    """
    Determines if user skill matches a job required skill phrase.
    Handles phrase equality, phrase containment, and high token overlap.
    """
    u = user_skill_phrase.lower().strip()
    j = job_skill_phrase.lower().strip()
    if u == j or u in j or j in u:
        return True

    u_words = set(re.findall(r'\b[a-z0-9]+\b', u))
    j_words = set(re.findall(r'\b[a-z0-9]+\b', j))
    if u_words and j_words:
        overlap = len(u_words & j_words) / max(len(j_words), 1)
        if overlap >= 0.75:
            return True

    return False


def analyze_skill_gap(user_skills_str, job_skills_str):
    """
    Analyzes required vs matched skills for a target job.
    Returns: (matched_list, missing_list, match_percentage_float)
    """
    user_skills = parse_skill_phrases(user_skills_str)
    job_skills = parse_skill_phrases(job_skills_str)

    if not job_skills:
        return [], [], 0.0

    matched = []
    missing = []

    for js in job_skills:
        found = False
        for us in user_skills:
            if is_skill_matched(us, js):
                found = True
                break
        if found:
            matched.append(js)
        else:
            missing.append(js)

    score_pct = len(matched) / len(job_skills)
    return matched, missing, score_pct


def calculate_what_if_score(user_skills_str, job_skills_str, added_skill):
    """Calculates new match percentage if the user learns a specific missing skill"""
    combined_skills = f"{user_skills_str}, {added_skill}"
    _, _, score = analyze_skill_gap(combined_skills, job_skills_str)
    return int(score * 100)


def find_best_course_for_missing_skill(missing_skill, all_courses):
    """
    Finds the most relevant free course specifically matching the missing skill.
    """
    ms = missing_skill.lower().strip()

    keyword_map = {
        'sql': ['sql', 'database', 'data science', 'python'],
        'python': ['python', 'full stack', 'data science'],
        'etl': ['data science', 'data engineer', 'python', 'sql'],
        'data warehousing': ['data science', 'database', 'sql', 'python'],
        'data pipelines': ['data science', 'python', 'web development'],
        'autocad': ['mechanical cad', 'cad', 'solidworks', 'civil'],
        'solidworks': ['mechanical cad', 'solidworks', 'cnc'],
        'cnc': ['cnc', 'manufacturing', 'mechanical'],
        'plc': ['automation', 'plc', 'electrical'],
        'automation': ['automation', 'plc', 'robotics'],
        'civil': ['civil', 'surveying', 'construction'],
        'electrical': ['electrical', 'solar', 'wiring'],
        'embedded': ['embedded', 'plc', 'electronics'],
        'iot': ['embedded', 'plc', 'electronics'],
        'data entry': ['computer', 'typing', 'ms office'],
    }

    targets = keyword_map.get(ms, [ms])
    best_course = None
    best_score = -1

    for c in all_courses:
        c_text = (c.get('title','') + ' ' + c.get('category','') + ' ' + c.get('skill_tags','') + ' ' + c.get('description','')).lower()
        score = 0
        for t in targets:
            if t in c_text:
                score += 3
        if ms in c_text:
            score += 5

        if score > best_score and score > 0:
            best_score = score
            best_course = c

    if not best_course and all_courses:
        best_course = all_courses[0]

    return best_course


def show_skill_gap(user, t):
    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon">📈</div>
        <div>
            <h2>Skill Gap Analysis & Learning Path</h2>
            <p>Analyze your profile skills against target job roles and get targeted course recommendations</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # User Profile Skills Banner
    user_skills_str = user.get('skills', 'No skills added yet')
    parsed_user_skills = parse_skill_phrases(user_skills_str)
    user_pills = " • ".join(parsed_user_skills) if parsed_user_skills else "None"

    st.markdown(f"""
    <div style="background:#161b22;border:1px solid #21262d;border-radius:12px;padding:1rem 1.25rem;margin-bottom:1.2rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
        <div style="display:flex;align-items:center;gap:1rem;">
            <div style="background:#1e3a5f;border:1px solid #2d4a8a;border-radius:50%;width:42px;height:42px;display:flex;align-items:center;justify-content:center;font-size:1.2rem;color:#60a5fa;">
                👤
            </div>
            <div>
                <div style="color:#e6edf3;font-weight:700;font-size:1.05rem;">{user['name']}</div>
                <div style="color:#8b949e;font-size:0.85rem;">🎯 Profile Skills: <b style="color:#34d399;">{user_pills}</b></div>
            </div>
        </div>
        <div>
            <span style="background:#0d2d1a;color:#34d399;border:1px solid #065f46;border-radius:20px;padding:4px 12px;font-size:0.82rem;font-weight:700;">
                {len(parsed_user_skills)} Verified Skills
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Fetch active jobs and free courses
    conn = get_conn()
    conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
    c = conn.cursor()

    c.execute("SELECT * FROM jobs WHERE is_active=1 ORDER BY id DESC")
    all_jobs = c.fetchall()

    c.execute("SELECT * FROM courses WHERE is_free=1 ORDER BY id DESC")
    all_courses = c.fetchall()
    conn.close()

    if not all_jobs:
        st.info("No active jobs available for Skill Gap Analysis.")
        return

    # Job Selection Dropdown
    best_matches_option = "🌟 Best Matches for Me (Top 5)"
    job_labels = [best_matches_option] + [f"{j['title']} at {j['company']} ({j['district']})" for j in all_jobs]
    selected_option = st.selectbox("🎯 Select Target Job Role for Gap Analysis", job_labels, key="sg_job_selectbox")

    target_jobs = []
    if selected_option == best_matches_option:
        for j in all_jobs:
            _, _, pct = analyze_skill_gap(user_skills_str, j['required_skills'])
            j['_score'] = pct
        target_jobs = sorted(all_jobs, key=lambda x: x['_score'], reverse=True)[:5]
    else:
        selected_idx = job_labels.index(selected_option) - 1
        target_jobs = [all_jobs[selected_idx]]

    # Display Skill Gap Analysis Cards
    for job in target_jobs:
        matched, missing, match_pct = analyze_skill_gap(user_skills_str, job['required_skills'])
        score_pct = int(match_pct * 100)
        req_skills_list = parse_skill_phrases(job['required_skills'])
        total_req_count = len(req_skills_list)
        matched_count = len(matched)

        if score_pct >= 70:
            bar_color = "#34d399"
            status_text = "🟢 Strong Fit"
        elif score_pct >= 40:
            bar_color = "#fbbf24"
            status_text = "🟡 Good Potential"
        else:
            bar_color = "#60a5fa"
            status_text = "🔵 Skill Upgrade Recommended"

        st.markdown(
            f'<div style="background:#161b22;border:1px solid #21262d;border-left:4px solid {bar_color};border-radius:14px;padding:1.25rem;margin-bottom:1.5rem;">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.75rem;margin-bottom:0.75rem;">'
            f'<div>'
            f'<div style="font-family:\'Sora\',sans-serif;font-weight:700;color:#e6edf3;font-size:1.15rem;">{job["title"]}</div>'
            f'<div style="color:#60a5fa;font-size:0.88rem;">🏢 {job["company"]} • 📍 {job["location"]}</div>'
            f'</div>'
            f'<div style="text-align:right;">'
            f'<span style="background:#0d1117;border:1px solid #21262d;border-radius:20px;padding:4px 12px;font-size:0.85rem;font-weight:700;color:{bar_color};">{status_text} • {score_pct}% Match</span>'
            f'<div style="color:#8b949e;font-size:0.78rem;margin-top:4px;">You have <b>{matched_count}</b> of <b>{total_req_count}</b> required skills</div>'
            f'</div>'
            f'</div>'

            f'<div style="background:#21262d;border-radius:6px;height:8px;margin-bottom:1rem;overflow:hidden;">'
            f'<div style="width:{score_pct}%;height:100%;background:{bar_color};transition:width 0.5s;"></div>'
            f'</div>',
            unsafe_allow_html=True
        )

        col_m1, col_m2 = st.columns(2)

        # Left Column: Matched Skills
        with col_m1:
            st.markdown("<b style='color:#34d399;font-size:0.9rem;'>✅ Skills You Have:</b>", unsafe_allow_html=True)
            if matched:
                pills_html = "".join([f"<span style='background:#0d2d1a;color:#34d399;border:1px solid #065f46;border-radius:6px;padding:3px 10px;font-size:0.8rem;margin:3px;display:inline-block;'>✓ {m}</span>" for m in matched])
                st.markdown(f"<div style='margin-top:0.4rem;margin-bottom:0.8rem;'>{pills_html}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='color:#8b949e;font-size:0.85rem;margin-top:0.4rem;'>No matching skills found in your profile yet.</div>", unsafe_allow_html=True)

        # Right Column: Missing Skills & What-if
        with col_m2:
            st.markdown("<b style='color:#f87171;font-size:0.9rem;'>❌ Missing Required Skills:</b>", unsafe_allow_html=True)
            if missing:
                for ms in missing:
                    what_if = calculate_what_if_score(user_skills_str, job['required_skills'], ms)
                    diff = what_if - score_pct
                    course = find_best_course_for_missing_skill(ms, all_courses)

                    st.markdown(
                        f'<div style="background:#0d1117;border:1px solid #21262d;border-radius:8px;padding:0.6rem 0.85rem;margin-top:0.4rem;margin-bottom:0.6rem;">'
                        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                        f'<span style="color:#f87171;font-weight:700;font-size:0.85rem;">❌ {ms}</span>'
                        f'<span style="color:#60a5fa;font-size:0.75rem;font-weight:600;">Match improves to {what_if}% (+{diff}%)</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    if course:
                        c_title = course.get('title', 'Free Course')
                        c_provider = course.get('provider', 'Govt Portal')
                        c_link = course.get('link', 'https://pmkvyofficial.org')

                        col_c1, col_c2 = st.columns([2.5, 1])
                        with col_c1:
                            st.markdown(f"<div style='color:#94a3b8;font-size:0.78rem;'>🎓 <b>Course:</b> {c_title} <span style='color:#60a5fa;'>({c_provider})</span></div>", unsafe_allow_html=True)
                        with col_c2:
                            if st.button(f"📚 Learn {ms}", key=f"learn_{job['id']}_{ms}", type="secondary", use_container_width=True):
                                st.toast(f"✅ Opening free course for {ms}!", icon="📚")
                                st.markdown(f"<script>window.open('{c_link}','_blank')</script>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("<div style='color:#34d399;font-size:0.85rem;margin-top:0.4rem;'>🎉 You have all required skills for this job!</div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
