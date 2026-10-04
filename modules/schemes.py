import streamlit as st
from modules.database import get_conn
from datetime import datetime

CATEGORY_ICONS = {
    "All": "🌐",
    "Housing": "🏠",
    "Education": "📚",
    "Employment": "💼",
    "Women": "👩",
    "Children": "👶",
    "Senior Citizens": "👵",
    "Health": "🏥",
    "Agriculture": "🌾",
    "Financial Assistance": "💰",
    "Disability": "♿",
    "MSME/Business": "🏭",
    "Students": "🎓"
}

def check_scheme_eligibility(user, scheme):
    """
    Evaluates scheme eligibility for a given user profile.
    Returns:
      status: "Eligible" | "Possibly Eligible" | "Not Eligible"
      reasons_matched: list of string descriptions for matching criteria
      reasons_failed: list of string descriptions for failing criteria
    """
    matched = []
    failed = []

    age = int(user.get('age', 0) or 0)
    income = int(user.get('income', 0) or 0)
    # Convert monthly income to annual if needed for scheme income limits
    annual_income = income * 12 if income < 50000 else income
    gender = user.get('gender', 'Male')
    caste = user.get('caste', 'General')
    state = user.get('state', 'Maharashtra')
    district = user.get('district', 'All')
    education = user.get('education', '8th Pass')

    # 1. Age Check
    min_age = int(scheme.get('min_age', 0) or 0)
    max_age = int(scheme.get('max_age', 100) or 100)
    if age >= min_age and age <= max_age:
        matched.append(f"Age {age} yrs is within required range ({min_age}–{max_age} yrs)")
    else:
        failed.append(f"Age must be between {min_age} and {max_age} yrs (Your age: {age})")

    # 2. Income Check
    max_inc = int(scheme.get('max_income', 9999999) or 9999999)
    if annual_income <= max_inc:
        matched.append(f"Annual income ₹{annual_income:,} is below limit of ₹{max_inc:,}")
    else:
        failed.append(f"Annual income (₹{annual_income:,}) exceeds limit of ₹{max_inc:,}")

    # 3. Gender Check
    sch_gender = scheme.get('gender', 'All')
    if sch_gender == 'All' or sch_gender == gender:
        matched.append(f"Gender '{gender}' matches requirement ({'Open for All' if sch_gender=='All' else sch_gender})")
    else:
        failed.append(f"Scheme is specifically reserved for {sch_gender} applicants")

    # 4. Caste / Category Check (ONLY restrict if scheme has explicit category restriction)
    sch_caste = scheme.get('caste', 'All')
    if sch_caste in ['All', '', None]:
        matched.append(f"Category '{caste}' is eligible (Open for All Categories: General, OBC, SC, ST, etc.)")
    else:
        allowed_castes = [c.strip().upper() for c in sch_caste.split(',')]
        if caste.strip().upper() in allowed_castes or 'ALL' in allowed_castes:
            matched.append(f"Category '{caste}' is listed in eligible categories ({sch_caste})")
        else:
            failed.append(f"Category '{caste}' not eligible. Reserved for: {sch_caste}")

    # 5. State / Location Check
    sch_state = scheme.get('state', 'All')
    if sch_state in ['All', '', None] or sch_state.lower() == state.lower():
        matched.append(f"State '{state}' is eligible for this scheme")
    else:
        failed.append(f"Available only in state: {sch_state} (Your state: {state})")

    # Determine overall status
    if len(failed) == 0:
        status = "Eligible"
    elif len(failed) == 1 and ("State" in failed[0] or "Annual income" in failed[0]):
        status = "Possibly Eligible"
    else:
        status = "Not Eligible"

    return status, matched, failed


def record_scheme_application(user_id, scheme_id):
    """Inserts a scheme application record into scheme_applications table if not present"""
    try:
        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT id FROM scheme_applications WHERE user_id=? AND scheme_id=?", (user_id, scheme_id))
        existing = c.fetchone()
        if not existing:
            c.execute("INSERT INTO scheme_applications (user_id, scheme_id, status, notes) VALUES (?, ?, 'Applied', 'Applied via Government Scheme Finder')",
                      (user_id, scheme_id))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error recording scheme application:", e)
        return False


def show_schemes(user, t):
    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon">🏛️</div>
        <div>
            <h2>Government Scheme Finder</h2>
            <p>Discover government benefits, subsidies, scholarships & pensions tailored to your profile</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # User Profile Overview Header Card
    annual_inc = int(user.get('income', 0) or 0) * 12 if int(user.get('income', 0) or 0) < 50000 else int(user.get('income', 0) or 0)
    st.markdown(f"""
    <div style="background:#161b22;border:1px solid #21262d;border-radius:12px;padding:1rem 1.25rem;margin-bottom:1.2rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
        <div style="display:flex;align-items:center;gap:1rem;">
            <div style="background:#1e3a5f;border:1px solid #2d4a8a;border-radius:50%;width:42px;height:42px;display:flex;align-items:center;justify-content:center;font-size:1.2rem;color:#60a5fa;">
                👤
            </div>
            <div>
                <div style="color:#e6edf3;font-weight:700;font-size:1.05rem;">{user['name']}</div>
                <div style="color:#8b949e;font-size:0.82rem;">📍 {user.get('district','N/A')}, {user.get('state','Maharashtra')}</div>
            </div>
        </div>
        <div style="display:flex;gap:1.2rem;flex-wrap:wrap;font-size:0.85rem;">
            <div>🎂 <span style="color:#8b949e;">Age:</span> <b style="color:#60a5fa;">{user.get('age','?')} yrs</b></div>
            <div>💰 <span style="color:#8b949e;">Annual Income:</span> <b style="color:#34d399;">₹{annual_inc:,}</b></div>
            <div>⚥ <span style="color:#8b949e;">Gender:</span> <b style="color:#60a5fa;">{user.get('gender','Male')}</b></div>
            <div>🏷️ <span style="color:#8b949e;">Category:</span> <b style="color:#a78bfa;">{user.get('caste','General')}</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Search & Filter Controls
    col_s1, col_s2, col_s3 = st.columns([2.2, 1.3, 1.5])
    with col_s1:
        search_query = st.text_input("🔍 Search Schemes", placeholder="Search by scheme name, benefit or category...", key="scheme_search_input")
    with col_s2:
        cat_options = list(CATEGORY_ICONS.keys())
        selected_cat = st.selectbox("📂 Filter Category", cat_options, key="scheme_category_sel")
    with col_s3:
        st.markdown("<div style='margin-top:1.8rem;'></div>", unsafe_allow_html=True)
        show_eligible_only = st.checkbox("✅ Show Eligible Only", value=True, key="scheme_elig_only_cb")

    # Fetch schemes from DB
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM schemes ORDER BY id ASC")
    raw_schemes = [dict(r) for r in c.fetchall()]
    conn.close()

    # Filter schemes based on search, category, and eligibility
    filtered_schemes = []
    total_eligible_count = 0
    total_possibly_count = 0

    for sch in raw_schemes:
        status, matched, failed = check_scheme_eligibility(user, sch)
        sch['elig_status'] = status
        sch['matched_reasons'] = matched
        sch['failed_reasons'] = failed

        if status == "Eligible":
            total_eligible_count += 1
        elif status == "Possibly Eligible":
            total_possibly_count += 1

        # Search Query filter
        if search_query:
            q = search_query.lower().strip()
            if q not in sch['name'].lower() and q not in sch['category'].lower() and q not in sch['benefits'].lower() and q not in sch['description'].lower():
                continue

        # Category Filter
        if selected_cat != "All" and sch['category'] != selected_cat:
            continue

        # Eligible Only Checkbox Filter
        if show_eligible_only and status == "Not Eligible":
            continue

        filtered_schemes.append(sch)

    # Summary bar
    st.markdown(f"""
    <div style="color:#8b949e;font-size:0.85rem;margin-bottom:1rem;">
        Found <b style="color:#34d399;">{len(filtered_schemes)}</b> schemes matching filters 
        (🟢 <b style="color:#34d399;">{total_eligible_count} Eligible</b> | 🟡 <b style="color:#fbbf24;">{total_possibly_count} Possibly Eligible</b> out of {len(raw_schemes)} total)
    </div>
    """, unsafe_allow_html=True)

    if not filtered_schemes:
        st.markdown("""
        <div style="background:#161b22;border:1px solid #21262d;border-radius:12px;padding:2.5rem;text-align:center;margin:1.5rem 0;">
            <div style="font-size:2.5rem;margin-bottom:0.75rem;">🏛️</div>
            <div style="color:#e6edf3;font-size:1.1rem;font-weight:600;">No schemes found matching your criteria</div>
            <div style="color:#8b949e;font-size:0.88rem;margin-top:0.3rem;">Try unchecking "Show Eligible Only" or clearing the search box.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Render Scheme Cards
    for sch in filtered_schemes:
        icon = CATEGORY_ICONS.get(sch['category'], "📋")
        status = sch['elig_status']

        if status == "Eligible":
            badge_html = '<span style="background:#0d2d1a;color:#34d399;border:1px solid #065f46;border-radius:20px;padding:3px 12px;font-weight:700;font-size:0.8rem;">🟢 Eligible</span>'
            border_color = '#059669'
            card_opacity = '1.0'
        elif status == "Possibly Eligible":
            badge_html = '<span style="background:#2d2000;color:#fbbf24;border:1px solid #78350f;border-radius:20px;padding:3px 12px;font-weight:700;font-size:0.8rem;">🟡 Possibly Eligible</span>'
            border_color = '#d97706'
            card_opacity = '0.95'
        else:
            badge_html = '<span style="background:#2d1515;color:#f87171;border:1px solid #7f1d1d;border-radius:20px;padding:3px 12px;font-weight:700;font-size:0.8rem;">❌ Not Eligible</span>'
            border_color = '#30363d'
            card_opacity = '0.75'

        st.markdown(
            f'<div style="background:#161b22;border:1px solid #21262d;border-left:4px solid {border_color};border-radius:12px;padding:1.25rem;margin-bottom:1rem;opacity:{card_opacity};">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.75rem;margin-bottom:0.6rem;">'
            f'  <div style="display:flex;align-items:center;gap:0.75rem;">'
            f'      <span style="font-size:1.6rem;">{icon}</span>'
            f'      <div>'
            f'          <div style="font-family:\'Sora\',sans-serif;font-weight:700;color:#e6edf3;font-size:1.1rem;">{sch["name"]}</div>'
            f'          <span style="background:#1e3a5f;color:#60a5fa;border:1px solid #2d4a8a;border-radius:6px;padding:2px 8px;font-size:0.72rem;font-weight:600;">{sch["category"]}</span>'
            f'      </div>'
            f'  </div>'
            f'  <div>{badge_html}</div>'
            f'</div>'
            f'<div style="color:#94a3b8;font-size:0.88rem;margin-bottom:0.6rem;line-height:1.4;">{sch["description"]}</div>'
            f'<div style="background:#0d1117;border:1px solid #21262d;border-radius:8px;padding:0.6rem 0.85rem;margin-bottom:0.75rem;color:#34d399;font-weight:600;font-size:0.88rem;">'
            f'  🎁 <b>Benefits:</b> {sch["benefits"]}'
            f'</div>'
            f'<div style="display:flex;flex-wrap:wrap;gap:0.8rem;color:#8b949e;font-size:0.8rem;margin-bottom:0.5rem;">'
            f'  <span>📋 <b>Target Group:</b> {sch["eligibility"]}</span>'
            f'  <span>📅 <b>Last Updated:</b> {sch.get("last_updated","01/10/2026")}</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        col_b1, col_b2 = st.columns([1, 1])
        with col_b1:
            with st.expander("❓ Why am I eligible / Matched Conditions"):
                if sch['matched_reasons']:
                    st.markdown("<b style='color:#34d399;font-size:0.85rem;'>✅ Matched Criteria:</b>", unsafe_allow_html=True)
                    for m in sch['matched_reasons']:
                        st.markdown(f"<div style='color:#e6edf3;font-size:0.82rem;margin-left:0.5rem;'>• {m}</div>", unsafe_allow_html=True)
                if sch['failed_reasons']:
                    st.markdown("<br><b style='color:#f87171;font-size:0.85rem;'>⚠️ Unmatched / Required Conditions:</b>", unsafe_allow_html=True)
                    for f in sch['failed_reasons']:
                        st.markdown(f"<div style='color:#f87171;font-size:0.82rem;margin-left:0.5rem;'>• {f}</div>", unsafe_allow_html=True)

        with col_b2:
            with st.expander("ℹ️ View Details & Application Guide"):
                st.markdown(f"""
                <div style="font-size:0.85rem;color:#e6edf3;line-height:1.5;">
                    <div style="margin-bottom:0.5rem;"><b style="color:#60a5fa;">📄 Required Documents:</b><br>{sch.get('document_required','Aadhaar Card, Income Proof, Bank Passbook')}</div>
                    <div style="margin-bottom:0.5rem;"><b style="color:#60a5fa;">📋 Application Process:</b><br><span style="white-space:pre-line;">{sch.get('app_process','Apply online on official website')}</span></div>
                    <div style="margin-bottom:0.5rem;"><b style="color:#60a5fa;">📞 Official Helpline:</b> {sch.get('helpline','1800-11-0001')}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Apply Online Button inside details
                if st.button(f"🌐 Visit Official Portal ({sch['name'][:20]}...)", key=f"portal_btn_{sch['id']}", use_container_width=True):
                    record_scheme_application(user['id'], sch['id'])
                    st.toast("✅ Application logged in your Application Tracker!", icon="📊")
                    st.markdown(f"[🔗 Open Official Government Portal: {sch['apply_link']}]({sch['apply_link']})")

        # Bottom Quick Action Apply Button
        if status in ["Eligible", "Possibly Eligible"]:
            col_a1, col_a2 = st.columns([1, 3])
            with col_a1:
                if st.button(f"🔗 Apply Online", key=f"apply_sch_{sch['id']}", type="primary", use_container_width=True):
                    record_scheme_application(user['id'], sch['id'])
                    st.toast("✅ Added to Application Tracker!", icon="📋")
                    st.success(f"✅ Application logged in Application Tracker! Opening Portal: {sch['apply_link']}")
                    st.markdown(f"<script>window.open('{sch['apply_link']}','_blank')</script>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
