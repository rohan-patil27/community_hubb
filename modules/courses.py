import streamlit as st
from modules.database import get_conn
import re

CAT_ICONS = {
    "All": "🌐",
    "IT/Software": "💻",
    "Data/AI": "🤖",
    "Electrical": "⚡",
    "Mechanical": "🔧",
    "Civil": "🏗️",
    "Healthcare": "🏥",
    "Agriculture": "🌾",
    "Business": "📊",
    "Tailoring": "🧵",
    "Carpentry": "🪚",
    "Digital Literacy": "📲",
    "Security": "🛡️",
}
CATEGORY_ICONS = CAT_ICONS

def calculate_course_skill_match(user_skills_str, course_tags_str):
    """
    Robust skill matching algorithm.
    Calculates phrase & word token overlaps between user's profile skills and course skill_tags.
    Returns float between 0.0 and 1.0.
    """
    if not user_skills_str or not course_tags_str:
        return 0.0

    u_raw = (user_skills_str or "").lower()
    c_raw = (course_tags_str or "").lower()

    # 1. Phrase extraction (comma separated)
    u_phrases = set(p.strip() for p in u_raw.split(',') if p.strip())
    c_phrases = set(p.strip() for p in c_raw.split(',') if p.strip())

    # 2. Token extraction (word boundaries)
    u_tokens = set(re.findall(r'\b[a-z0-9]+\b', u_raw))
    c_tokens = set(re.findall(r'\b[a-z0-9]+\b', c_raw))

    if not c_tokens and not c_phrases:
        return 0.0

    # Phrase match calculation
    matched_phrases = 0
    for cp in c_phrases:
        if any(cp in up or up in cp for up in u_phrases):
            matched_phrases += 1
    phrase_score = matched_phrases / max(len(c_phrases), 1)

    # Token match calculation
    matched_tokens = u_tokens & c_tokens
    token_score = len(matched_tokens) / max(len(c_tokens), 1)

    # Take maximum score & clamp to 1.0
    final_score = max(phrase_score, token_score)
    return round(min(final_score, 1.0), 2)


def parse_duration_months(duration_str):
    """Parses duration string into numeric months for sorting"""
    if not duration_str: return 99
    match = re.search(r'(\d+)', duration_str)
    if match:
        val = int(match.group(1))
        if 'week' in duration_str.lower():
            return val / 4.0
        return float(val)
    return 99.0


def show_courses(user, t):
    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon">🎓</div>
        <div>
            <h2>Free Skill Courses</h2>
            <p>PMKVY, Skill India, NIELIT & Swayam Free Vocational & Technical Certification Programs</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Free Banner
    user_skills_display = user.get('skills', 'No skills added yet')
    st.markdown(f"""
    <div style="background:#1a2744;border:1px solid #2d4a8a;border-radius:12px;padding:1rem 1.25rem;margin-bottom:1.2rem;display:flex;gap:1rem;align-items:center;flex-wrap:wrap;">
        <div style="font-size:2rem;background:#1e3a5f;border-radius:50%;width:48px;height:48px;display:flex;align-items:center;justify-content:center;color:#60a5fa;">🆓</div>
        <div style="flex:1;">
            <div style="color:#e6edf3;font-weight:700;font-size:1rem;">100% Free Govt Vocational & Technical Courses</div>
            <div style="color:#94a3b8;font-size:0.85rem;margin-top:2px;">
                Your Profile Skills: <b style="color:#34d399;">{user_skills_display}</b> — AI matches free courses to help upgrade your career.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Database Fetch
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM courses WHERE is_free=1 ORDER BY id DESC")
    courses = [dict(r) for r in c.fetchall()]
    conn.close()

    # Calculate skill match score for all courses
    user_skills = user.get('skills', '')
    for course in courses:
        course['_score'] = calculate_course_skill_match(user_skills, course.get('skill_tags', ''))
        course['_dur_months'] = parse_duration_months(course.get('duration', ''))

    # Filters Row
    col_f1, col_f2, col_f3, col_f4 = st.columns([2, 1.2, 1.2, 1.3])
    with col_f1:
        search_query = st.text_input("🔍 Search Courses", placeholder="Search courses by skill, course name...", key="course_search")
    with col_f2:
        available_cats = ["All"] + list(CATEGORY_ICONS.keys())[1:]
        sel_cat = st.selectbox("📂 Category", available_cats, key="course_cat")
    with col_f3:
        all_langs = ["All"] + sorted(list(set(c['language'] for c in courses if c.get('language'))))
        sel_lang = st.selectbox("🌐 Language", all_langs, key="course_lang")
    with col_f4:
        sort_by = st.selectbox("📊 Sort By", ["Best Match (AI)", "Newest", "Shortest Duration", "A-Z"], key="course_sort")

    # Filter Logic
    filtered_courses = courses
    if search_query:
        q = search_query.lower().strip()
        filtered_courses = [
            crs for crs in filtered_courses
            if q in crs['title'].lower() or q in crs['category'].lower() or q in crs.get('skill_tags','').lower() or q in crs.get('description','').lower() or q in crs.get('provider','').lower()
        ]

    if sel_cat != "All":
        filtered_courses = [crs for crs in filtered_courses if crs['category'] == sel_cat]

    if sel_lang != "All":
        filtered_courses = [crs for crs in filtered_courses if sel_lang.lower() in crs['language'].lower()]

    # Sorting Logic
    if sort_by == "Best Match (AI)":
        filtered_courses.sort(key=lambda x: (x['_score'], x['id']), reverse=True)
    elif sort_by == "Newest":
        filtered_courses.sort(key=lambda x: x['id'], reverse=True)
    elif sort_by == "Shortest Duration":
        filtered_courses.sort(key=lambda x: x['_dur_months'])
    elif sort_by == "A-Z":
        filtered_courses.sort(key=lambda x: x['title'])

    st.markdown(f"<div style='color:#8b949e;font-size:0.85rem;margin-bottom:1rem;'>Showing <b style='color:#60a5fa;'>{len(filtered_courses)}</b> free certified courses</div>", unsafe_allow_html=True)

    if not filtered_courses:
        st.markdown("""
        <div style="background:#161b22;border:1px solid #21262d;border-radius:12px;padding:2.5rem;text-align:center;margin:1.5rem 0;">
            <div style="font-size:2.5rem;margin-bottom:0.75rem;">🎓</div>
            <div style="color:#e6edf3;font-size:1.1rem;font-weight:600;">No courses found matching your filters</div>
            <div style="color:#8b949e;font-size:0.88rem;margin-top:0.3rem;">Try searching for a different skill or select "All" categories.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Render Course Cards Grid (2 Columns)
    col_left, col_right = st.columns(2)

    for idx, course in enumerate(filtered_courses):
        score_pct = int(course['_score'] * 100)
        icon = CAT_ICONS.get(course['category'], "📚")

        if score_pct >= 60:
            match_color = "#34d399"
            match_bg = "#0d2d1a"
            match_border = "#065f46"
            badge_text = f"🎯 {score_pct}% Match (High)"
        elif score_pct >= 30:
            match_color = "#fbbf24"
            match_bg = "#2d2000"
            match_border = "#78350f"
            badge_text = f"🎯 {score_pct}% Match"
        elif score_pct > 0:
            match_color = "#60a5fa"
            match_bg = "#1e3a5f"
            match_border = "#2d4a8a"
            badge_text = f"🎯 {score_pct}% Match"
        else:
            match_color = "#8b949e"
            match_bg = "#21262d"
            match_border = "#30363d"
            badge_text = "🎯 Skill Recommended"

        level = course.get('level', 'Beginner')
        certificate = course.get('certificate', 'NSDC / Govt Certified')
        provider = course.get('provider', 'PMKVY / Skill India')
        skills_pills = ", ".join([s.strip().title() for s in course.get('skill_tags','').split(',') if s.strip()])

        card_html = (
            f'<div style="background:#161b22;border:1px solid #21262d;border-left:4px solid {match_color};border-radius:14px;padding:1.25rem;margin-bottom:1rem;display:flex;flex-direction:column;justify-content:space-between;min-height:280px;">'
            f'<div>'
            f'<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:0.5rem;margin-bottom:0.6rem;">'
            f'<div style="display:flex;align-items:center;gap:0.65rem;">'
            f'<span style="font-size:1.6rem;">{icon}</span>'
            f'<div>'
            f'<div style="font-family:\'Sora\',sans-serif;font-weight:700;color:#e6edf3;font-size:1rem;line-height:1.3;">{course["title"]}</div>'
            f'<div style="color:#60a5fa;font-size:0.8rem;margin-top:2px;">🏛️ {provider}</div>'
            f'</div>'
            f'</div>'
            f'<span style="background:{match_bg};color:{match_color};border:1px solid {match_border};border-radius:20px;padding:3px 10px;font-size:0.75rem;font-weight:700;white-space:nowrap;">{badge_text}</span>'
            f'</div>'
            f'<div style="color:#94a3b8;font-size:0.85rem;margin-bottom:0.75rem;line-height:1.45;">{course["description"]}</div>'
            f'<div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin-bottom:0.75rem;">'
            f'<span style="background:#1e3a5f;color:#60a5fa;border:1px solid #2d4a8a;border-radius:6px;padding:3px 8px;font-size:0.75rem;">📂 {course["category"]}</span>'
            f'<span style="background:#2d1b69;color:#a78bfa;border:1px solid #4c1d95;border-radius:6px;padding:3px 8px;font-size:0.75rem;">⏱️ {course["duration"]}</span>'
            f'<span style="background:#0d2d1a;color:#34d399;border:1px solid #065f46;border-radius:6px;padding:3px 8px;font-size:0.75rem;">📊 {level}</span>'
            f'<span style="background:#21262d;color:#e6edf3;border:1px solid #30363d;border-radius:6px;padding:3px 8px;font-size:0.75rem;">🌐 {course["language"]}</span>'
            f'</div>'
            f'<div style="background:#0d1117;border:1px solid #21262d;border-radius:8px;padding:0.5rem 0.75rem;margin-bottom:0.6rem;font-size:0.78rem;color:#34d399;font-weight:600;">{certificate}</div>'
            f'<div style="color:#8b949e;font-size:0.78rem;margin-bottom:0.5rem;">🔧 <b>Skills Learned:</b> <span style="color:#60a5fa;">{skills_pills}</span></div>'
            f'</div>'
            f'</div>'
        )

        target_col = col_left if idx % 2 == 0 else col_right
        with target_col:
            st.markdown(card_html, unsafe_allow_html=True)
            
            c1, c2 = st.columns([1, 1])
            with c1:
                with st.expander("ℹ️ Course Details"):
                    st.markdown(f"""
                    <div style="font-size:0.82rem;color:#e6edf3;line-height:1.5;">
                        <div style="margin-bottom:0.4rem;"><b style="color:#60a5fa;">🏛️ Official Training Provider:</b> {provider}</div>
                        <div style="margin-bottom:0.4rem;"><b style="color:#60a5fa;">📜 Certificate Awarded:</b> {certificate}</div>
                        <div style="margin-bottom:0.4rem;"><b style="color:#60a5fa;">⏱️ Program Duration:</b> {course['duration']} ({level})</div>
                        <div style="margin-bottom:0.4rem;"><b style="color:#60a5fa;">🌐 Mode / Language:</b> Free Govt Training ({course['language']})</div>
                        <div style="margin-bottom:0.4rem;"><b style="color:#60a5fa;">💼 Placement Assistance:</b> Job placement support upon successful assessment.</div>
                    </div>
                    """, unsafe_allow_html=True)
            with c2:
                if st.button(f"🔗 Apply / Enroll Now", key=f"course_enroll_{course['id']}", type="primary", use_container_width=True):
                    st.toast("✅ Opening official course portal!", icon="🎓")
                    st.success(f"✅ Opening Portal: {course.get('link','https://pmkvyofficial.org')}")
                    st.markdown(f"<script>window.open('{course.get('link','https://pmkvyofficial.org')}','_blank')</script>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

