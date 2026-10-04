import streamlit as st
import os, base64

logo_image_path = os.path.join(os.path.dirname(__file__), 'logo.png')
page_icon_val = logo_image_path if os.path.exists(logo_image_path) else "🌟"

st.set_page_config(
    page_title="Community Hub",
    page_icon=page_icon_val,
    layout="wide",
    initial_sidebar_state="expanded"
)

if os.path.exists(logo_image_path):
    with open(logo_image_path, "rb") as f:
        b64_logo = base64.b64encode(f.read()).decode()
    logo_sidebar_html = f"<img src='data:image/png;base64,{b64_logo}' style='width:150px;height:auto;margin-bottom:0.4rem;filter:drop-shadow(0 6px 18px rgba(0,0,0,0.5)) drop-shadow(0 0 12px rgba(59,130,246,0.3));' />"
    logo_header_html  = f"<img src='data:image/png;base64,{b64_logo}' style='width:85px;height:auto;vertical-align:middle;margin-right:16px;filter:drop-shadow(0 4px 14px rgba(0,0,0,0.5)) drop-shadow(0 0 10px rgba(59,130,246,0.3));' />"
else:
    logo_sidebar_html = "<div style='font-size:2.5rem;'>🌟</div>"
    logo_header_html  = "<div class='header-icon'>🌟</div>"

from modules.database import init_db, get_unread_alerts_count
from modules.auth import show_login, show_register
from modules.job_matching import show_job_matching
from modules.schemes import show_schemes
from modules.emergency import show_emergency
from modules.resume import show_resume_generator
from modules.admin import show_admin_dashboard
from modules.tracker import show_tracker
from modules.courses import show_courses
from modules.skill_gap import show_skill_gap
from modules.chatbot import show_chatbot
from modules.profile import show_user_profile
from modules.notifications import show_notifications
import sys, importlib
if 'modules.language' in sys.modules:
    importlib.reload(sys.modules['modules.language'])
if 'modules.chatbot' in sys.modules:
    importlib.reload(sys.modules['modules.chatbot'])
from modules.language import get_text
from modules.styles import load_styles

init_db()
load_styles()

if 'user'     not in st.session_state: st.session_state.user     = None
if 'language' not in st.session_state: st.session_state.language = 'english'
if 'page'     not in st.session_state: st.session_state.page     = 'home'

def t(key):
    return get_text(key, st.session_state.language)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='text-align:center;padding:1rem 0 0.5rem;'>"
        + logo_sidebar_html +
        "<div style='font-weight:700;color:#e6edf3;font-size:0.95rem;margin-top:0.4rem;'>"
        "Community Hub</div></div>",
        unsafe_allow_html=True
    )

    st.markdown("### 🌐 Language")
    languages = {
        'english': 'English',
        'hindi': 'Hindi (हिंदी)',
        'marathi': 'Marathi (मराठी)',
        'gujarati': 'Gujarati (ગુજરાતી)',
        'bengali': 'Bengali (বাংলা)',
        'tamil': 'Tamil (தமிழ்)',
        'telugu': 'Telugu (తెలుగు)',
        'kannada': 'Kannada (ಕನ್ನಡ)',
        'malayalam': 'Malayalam (മലയാളം)',
        'punjabi': 'Punjabi (ਪੰਜਾਬੀ)',
        'urdu': 'Urdu (اردو)',
        'sanskrit': 'Sanskrit (संस्कृतम्)',
        'sindhi': 'Sindhi (سنڌي)'
    }
    lang_options = list(languages.values())
    current_lang_name = languages.get(st.session_state.language, 'English')
    lang_idx = lang_options.index(current_lang_name) if current_lang_name in lang_options else 0
    
    selected_lang = st.selectbox("", lang_options, index=lang_idx, key="lang_select", label_visibility="collapsed")
    
    for k, v in languages.items():
        if v == selected_lang:
            st.session_state.language = k
            break

    st.markdown("---")

    if st.session_state.user:
        u = st.session_state.user
        gender_icon = "👨‍💼" if u.get('gender') == 'Male' else "👩‍💼"
        user_role   = "⚙️ Admin" if u.get('is_admin') else "👤 User"
        st.markdown(
            "<div style='background:#1a2332;border:1px solid #2d4a8a;border-radius:10px;"
            "padding:1rem;text-align:center;'>"
            "<div style='font-size:2rem;'>" + gender_icon + "</div>"
            "<div style='font-weight:600;color:#e6edf3;margin-top:0.3rem;'>" + str(u.get('name','')) + "</div>"
            "<div style='color:#8b949e;font-size:0.8rem;'>" + str(u.get('location','')) + "</div>"
            "<div style='margin-top:0.4rem;font-size:0.72rem;color:#60a5fa;'>" + user_role + "</div>"
            "</div>",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)

        u_count = get_unread_alerts_count(u['id'])
        alert_txt = t("nav_alerts").replace("🔔 ","")
        alert_label = f"🔔 {alert_txt} ({u_count})" if u_count > 0 else f"🔔 {alert_txt}"

        nav_pages = [
            ("👤 " + t("nav_profile").replace("👤 ",""),         "profile"),
            (alert_label,                                       "notifications"),
            ("💼 " + t("nav_jobs").replace("💼 ",""),           "jobs"),
            ("🏛️ " + t("nav_schemes").replace("🏛️ ",""),        "schemes"),
            ("📊 " + t("nav_tracker").replace("📊 ",""),         "tracker"),
            ("🎓 " + t("nav_courses").replace("🎓 ",""),         "courses"),
            ("📈 " + t("nav_skillgap").replace("📈 ",""),       "skillgap"),
            ("🎙️ " + t("nav_chatbot").replace("🎙️ ",""),        "chatbot"),
            ("📄 " + t("nav_resume").replace("📄 ",""),         "resume"),
            ("🆘 " + t("nav_emergency").replace("🆘 ",""),      "emergency"),
        ]
        if u.get('is_admin'):
            nav_pages.append(("⚙️ " + t("nav_admin").replace("⚙️ ",""), "admin"))
        for label, pg in nav_pages:
            b_type = "primary" if st.session_state.page == pg else "secondary"
            if st.button(label, key="side_"+pg, use_container_width=True, type=b_type):
                st.session_state.page = pg
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(t("nav_logout"), use_container_width=True, key="side_logout"):
            st.session_state.user = None
            st.session_state.page = 'home'
            st.rerun()
    else:
        for label, pg in [("🏠 " + t("nav_home").replace("🏠 ",""),"home"),
                          ("🎙️ " + t("nav_chatbot").replace("🎙️ ",""),"chatbot"),
                          ("🔐 " + t("login"),"login"),
                          ("📝 " + t("register"),"register"),
                          ("🆘 " + t("nav_emergency").replace("🆘 ",""),"emergency")]:
            b_type = "primary" if st.session_state.page == pg else "secondary"
            if st.button(label, key="side_"+pg, use_container_width=True, type=b_type):
                st.session_state.page = pg
                st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='color:#94a3b8;font-size:0.78rem;text-align:center;line-height:1.5;padding:0.4rem 0;'>"
        "<span style='color:#3b82f6;font-weight:600;'>One Platform</span> · "
        "<span style='color:#10b981;font-weight:600;'>One Connection</span><br>"
        "<span style='color:#f59e0b;font-weight:600;'>Multiple Opportunities</span>"
        "</div>",
        unsafe_allow_html=True
    )

# ── Header ────────────────────────────────────────────────────────────────────
_title    = t('app_title')
_subtitle = t('app_subtitle')
st.markdown(
    "<div class='main-header'><div class='header-content'>"
    + logo_header_html +
    "<div><h1>" + _title + "</h1><p>" + _subtitle + "</p></div>"
    "</div></div>",
    unsafe_allow_html=True
)

# ── Top Nav ────────────────────────────────────────────────────────────────────
if st.session_state.user:
    u = st.session_state.user
    u_count = get_unread_alerts_count(u['id'])
    alert_txt = t("nav_alerts").replace("🔔 ","")
    alert_label = f"🔔 {alert_txt} ({u_count})" if u_count > 0 else f"🔔 {alert_txt}"

    nav_items = [
        ("👤 " + t("nav_profile").replace("👤 ",""), "profile"),
        (alert_label, "notifications"),
        ("💼 " + t("nav_jobs").replace("💼 ",""), "jobs"),
        ("🏛️ " + t("nav_schemes").replace("🏛️ ",""), "schemes"),
        ("📊 " + t("nav_tracker").replace("📊 ",""), "tracker"),
        ("🎓 " + t("nav_courses").replace("🎓 ",""), "courses"),
        ("📈 " + t("nav_skillgap").replace("📈 ",""), "skillgap"),
        ("🎙️ " + t("nav_chatbot").replace("🎙️ ",""), "chatbot"),
        ("📄 " + t("nav_resume").replace("📄 ",""), "resume"),
        ("🆘 " + t("nav_emergency").replace("🆘 ",""), "emergency"),
    ]
    if u.get('is_admin'): nav_items.append(("⚙️ " + t("nav_admin").replace("⚙️ ",""),"admin"))
    nav_items.append((t("nav_logout"),"logout"))
    cols = st.columns(len(nav_items))
    for col,(label,pg) in zip(cols, nav_items):
        with col:
            b_type = "primary" if st.session_state.page == pg else "secondary"
            if st.button(label, key="topnav_"+pg, use_container_width=True, type=b_type):
                if pg == "logout":
                    st.session_state.user = None
                    st.session_state.page = 'home'
                else:
                    st.session_state.page = pg
                st.rerun()
else:
    cols = st.columns(5)
    for col,(label,pg) in zip(cols,[("🏠 " + t("nav_home").replace("🏠 ",""),"home"),
                                     ("🎙️ " + t("nav_chatbot").replace("🎙️ ",""),"chatbot"),
                                     ("🔐 " + t("login"),"login"),
                                     ("📝 " + t("register"),"register"),
                                     ("🆘 " + t("nav_emergency").replace("🆘 ",""),"emergency")]):
        with col:
            b_type = "primary" if st.session_state.page == pg else "secondary"
            if st.button(label, key="topnav_"+pg, use_container_width=True, type=b_type):
                st.session_state.page = pg
                st.rerun()

st.markdown("---")

# ── Page Router ───────────────────────────────────────────────────────────────
page = st.session_state.page

if page == 'home':
    hero_title = t('hero_title')
    st.markdown(
        "<div class='hero-section'><h2>" + hero_title + "</h2></div>",
        unsafe_allow_html=True
    )

    c1,c2,c3,c4 = st.columns(4)
    for col,(icon,num,lbl) in zip([c1,c2,c3,c4],[
        ("💼","500+",t('stat_jobs')),("🏛️","10+",t('stat_schemes')),
        ("🏥","12+",t('stat_ngos')),("👥","1000+",t('stat_users'))]):
        with col:
            st.markdown(
                "<div class='stat-card'><div class='stat-icon'>" + icon + "</div>"
                "<div class='stat-num'>" + num + "</div>"
                "<div class='stat-label'>" + lbl + "</div></div>",
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    feats_l = [
        ("🎯", t('feat_job_title'),     t('feat_job_desc')),
        ("🎙️", t('feat_chatbot_title'), t('feat_chatbot_desc')),
        ("📊", t('feat_tracker_title'), t('feat_tracker_desc')),
        ("📄", t('feat_resume_title'),  t('feat_resume_desc')),
    ]
    feats_r = [
        ("🏛️", t('feat_scheme_title'),    t('feat_scheme_desc')),
        ("🎓", t('feat_courses_title'),   t('feat_courses_desc')),
        ("📈", t('feat_skillgap_title'),  t('feat_skillgap_desc')),
        ("🆘", t('feat_emergency_title'), t('feat_emergency_desc')),
    ]
    for col, feats in [(col_l, feats_l),(col_r, feats_r)]:
        with col:
            for icon, title, desc in feats:
                st.markdown(
                    "<div class='feature-card'><h3>" + icon + " " + title + "</h3>"
                    "<p>" + desc + "</p></div>",
                    unsafe_allow_html=True
                )

    st.markdown(
        "<div style='background:#1a2744;border:1px solid #2d4a8a;border-radius:14px;"
        "padding:1.2rem;margin-top:0.75rem;text-align:center;'>"
        "<div style='font-size:1.3rem;margin-bottom:0.4rem;'>🌐</div>"
        "<div style='color:#e6edf3;font-weight:600;margin-bottom:0.2rem;'>Available in 23 Languages</div>"
        "<div style='color:#8b949e;font-size:0.88rem;'>English · हिंदी · मराठी · ગુજરાતી · বাংলা · தமிழ் · తెలుగు · ಕನ್ನಡ · മലയാളം · پੰਜਾਬੀ · اردو · ଓଡ଼ିଆ — Switch from sidebar</div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,2,1])
    with c2:
        if st.button("🚀 " + t('get_started'), use_container_width=True, type="primary", key="home_cta"):
            st.session_state.page = 'register'
            st.rerun()

elif page == 'login':    show_login(t)
elif page == 'register': show_register(t)
elif page == 'emergency': show_emergency(t)

elif page == 'notifications':
    if st.session_state.user: show_notifications(st.session_state.user, t)
    else:
        st.warning("Please login first.")
        st.session_state.page = 'login'; st.rerun()

elif page == 'profile':
    if st.session_state.user: show_user_profile(st.session_state.user, t)
    else:
        st.warning("Please login first.")
        st.session_state.page = 'login'; st.rerun()

elif page == 'jobs':
    if st.session_state.user: show_job_matching(st.session_state.user, t)
    else:
        st.warning("Please login first.")
        st.session_state.page = 'login'; st.rerun()

elif page == 'schemes':
    if st.session_state.user: show_schemes(st.session_state.user, t)
    else:
        st.warning("Please login first.")
        st.session_state.page = 'login'; st.rerun()

elif page == 'tracker':
    if st.session_state.user: show_tracker(st.session_state.user, t)
    else:
        st.warning("Please login first.")
        st.session_state.page = 'login'; st.rerun()

elif page == 'courses':
    if st.session_state.user: show_courses(st.session_state.user, t)
    else:
        st.warning("Please login first.")
        st.session_state.page = 'login'; st.rerun()

elif page == 'skillgap':
    if st.session_state.user: show_skill_gap(st.session_state.user, t)
    else:
        st.warning("Please login first.")
        st.session_state.page = 'login'; st.rerun()

elif page == 'chatbot':
    show_chatbot(st.session_state.user, t, key_prefix="page_cb")

elif page == 'resume':
    if st.session_state.user: show_resume_generator(st.session_state.user, t)
    else:
        st.warning("Please login first.")
        st.session_state.page = 'login'; st.rerun()

elif page == 'admin':
    if st.session_state.user and st.session_state.user.get('is_admin'):
        show_admin_dashboard(t)
    else:
        st.error("Admin access only.")
        st.session_state.page = 'home'; st.rerun()

# ── Floating Doraemon AI Chatbot FAB ──────────────────────────────────────────
bot_image_path = os.path.join(os.path.dirname(__file__), 'bot.png')
if os.path.exists(bot_image_path):
    with open(bot_image_path, "rb") as f:
        b64_img = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <style>
    div[data-testid="stPopover"] {{
        position: fixed !important;
        bottom: 30px !important;
        right: 30px !important;
        left: auto !important;
        width: 80px !important;
        height: 80px !important;
        z-index: 999999 !important;
        display: block !important;
    }}
    div[data-testid="stPopover"] * {{
        width: auto !important;
        min-width: 0 !important;
    }}
    div[data-testid="stPopover"] button {{
        background-image: url('data:image/png;base64,{b64_img}') !important;
        background-size: contain !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-color: transparent !important;
        color: transparent !important;
        border-radius: 50% !important;
        width: 80px !important;
        height: 80px !important;
        padding: 0 !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        display: block !important;
    }}
    div[data-testid="stPopover"] button * {{
        display: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

with st.popover("🤖 Ask AI", key="chatbot_fab"):
    show_chatbot(st.session_state.user, t, key_prefix="fab_cb")

