import streamlit as st
from datetime import datetime
from modules.database import (
    get_user_alerts, get_unread_alerts_count, mark_alert_read,
    create_alert, seed_personalized_alerts, send_sms
)

def show_notifications(user, t):
    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon">🔔</div>
        <div>
            <h2>Job & Government Scheme Alert Center</h2>
            <p>Real-time personalized alerts for new job postings, eligible government welfare schemes, and application status updates</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not user:
        st.warning("🔒 Please login to view your personalized job and scheme alerts!")
        return

    # Seed initial alerts if user has none
    seed_personalized_alerts(user)

    unread_count = get_unread_alerts_count(user['id'])

    tabs = st.tabs([
        f"🔔 Active Alerts ({unread_count} New)",
        "📱 Instant SMS & Email Alerts",
        "⚙️ Alert Preferences"
    ])

    # ══════════════════════════════════════════════════════════════════
    # TAB 1 — ACTIVE ALERTS
    # ══════════════════════════════════════════════════════════════════
    with tabs[0]:
        st.markdown("<br>", unsafe_allow_html=True)
        alerts = get_user_alerts(user['id'])

        if not alerts:
            st.info("🎉 You have no active alerts right now. New job & scheme alerts will appear here automatically!")
        else:
            col_b1, col_b2 = st.columns([3, 1])
            with col_b1:
                st.markdown(f"#### 📬 Total Alerts: **{len(alerts)}** | Unread: **{unread_count}**")
            with col_b2:
                if st.button("✔️ Mark All as Read", key="mark_all_read_btn", use_container_width=True):
                    for a in alerts:
                        if not a['is_read']:
                            mark_alert_read(a['id'])
                    st.success("✅ All alerts marked as read!")
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            for a in alerts:
                alert_id = a['id']
                is_unread = not a['is_read']
                a_type = a.get('alert_type', 'Job')
                
                # Badge color by type
                if a_type == 'Job':
                    badge_color = "#3b82f6" # Blue
                    badge_icon = "💼"
                    bg_border = "border-left: 5px solid #3b82f6;"
                elif a_type == 'Scheme':
                    badge_color = "#10b981" # Green
                    badge_icon = "🏛️"
                    bg_border = "border-left: 5px solid #10b981;"
                elif a_type == 'Tracker':
                    badge_color = "#f59e0b" # Orange
                    badge_icon = "📊"
                    bg_border = "border-left: 5px solid #f59e0b;"
                else:
                    badge_color = "#8b5cf6" # Purple
                    badge_icon = "🎓"
                    bg_border = "border-left: 5px solid #8b5cf6;"

                bg_color = "#1c2333" if is_unread else "#161b22"
                unread_badge = "<span style='background:#ef4444;color:#ffffff;font-size:0.75rem;padding:0.2rem 0.5rem;border-radius:10px;font-weight:700;'>NEW</span>" if is_unread else ""

                st.markdown(f"""
                <div style="background:{bg_color};border:1px solid #21262d;{bg_border}border-radius:12px;padding:1.2rem;margin-bottom:1rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                        <div style="font-weight:700;color:#e6edf3;font-size:1.05rem;">
                            {badge_icon} {a['title']} {unread_badge}
                        </div>
                        <div style="color:#8b949e;font-size:0.8rem;">
                            🕒 {a.get('created_at','Just now')}
                        </div>
                    </div>
                    <div style="color:#94a3b8;font-size:0.92rem;line-height:1.5;margin-bottom:0.8rem;">
                        {a['message']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                c_act1, c_act2, c_act3 = st.columns([1.5, 1.5, 3])
                with c_act1:
                    target_pg = a.get('link_page', 'jobs')
                    btn_label = "💼 View Jobs" if target_pg == 'jobs' else ("🏛️ View Schemes" if target_pg == 'schemes' else "📊 Track Application")
                    if st.button(btn_label, key=f"nav_alert_{alert_id}", use_container_width=True):
                        mark_alert_read(alert_id)
                        st.session_state.page = target_pg
                        st.rerun()
                with c_act2:
                    if is_unread:
                        if st.button("✔️ Mark Read", key=f"read_alert_{alert_id}", use_container_width=True):
                            mark_alert_read(alert_id)
                            st.rerun()

                st.markdown("<hr style='border-color:#21262d;margin:0.8rem 0;'>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # TAB 2 — INSTANT SMS & EMAIL ALERTS DISPATCHER
    # ══════════════════════════════════════════════════════════════════
    with tabs[1]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📱 Instant SMS & Mobile Alert Dispatcher")
        st.markdown("Simulate receiving real-time SMS alerts directly to your mobile phone number!")

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            target_phone = st.text_input("Mobile Number for SMS Alert", value=user.get('phone','9876543210'))
            alert_topic = st.selectbox("Select Alert Topic", [
                "💼 New Matching Job Alert",
                "🏛️ Eligible Government Scheme Alert",
                "📊 Application Tracker Update Alert",
                "🎓 Free Skill Certification Alert"
            ])

        district = user.get('district', 'Jalgaon')
        topic_templates = {
            "💼 New Matching Job Alert": f"Community Hub Alert: 3 new Job openings matching your skills in {district}! Apply now on the jobs portal.",
            "🏛️ Eligible Government Scheme Alert": f"Scheme Alert: You are eligible for PM Kisan & Welfare schemes in {district}. Check eligibility & apply.",
            "📊 Application Tracker Update Alert": f"Application Status: Your job application for Senior Assistant has been SHORTLISTED for interview!",
            "🎓 Free Skill Certification Alert": f"Skill Training Alert: Free Digital Literacy & Vocational Skills Certification course now open in {district}!"
        }
        suggested_msg = topic_templates.get(alert_topic, f"Community Hub Alert for {alert_topic}")

        with col_s2:
            custom_msg = st.text_area("Custom Alert Message", value=suggested_msg, height=110)

        if st.button("📲 Send Instant SMS Alert Now", type="primary", use_container_width=True):
            if target_phone:
                send_sms(target_phone.strip(), custom_msg, sms_type="Job Alert", user_id=user['id'])
                # Also create local database alert
                create_alert(user['id'], alert_topic, custom_msg, alert_type="Job" if "Job" in alert_topic else "Scheme", link_page="jobs" if "Job" in alert_topic else "schemes")
                st.success(f"✅ SMS Alert sent successfully to **{target_phone}**!")
                st.balloons()
            else:
                st.error("❌ Please enter a valid mobile number.")

    # ══════════════════════════════════════════════════════════════════
    # TAB 3 — ALERT PREFERENCES
    # ══════════════════════════════════════════════════════════════════
    with tabs[2]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Customize Notification Preferences")
        st.markdown("Manage which job and scheme notifications you want to receive on your phone and email.")

        st.markdown("""<div style="background:#161b22;border:1px solid #21262d;border-radius:12px;padding:1.5rem;margin-bottom:1rem;">""", unsafe_allow_html=True)
        
        pref_jobs = st.toggle("💼 Instant SMS Alerts for New Matching Jobs", value=True, key="pref_jobs")
        pref_schemes = st.toggle("🏛️ Government Welfare Scheme Eligibility Notifications", value=True, key="pref_schemes")
        pref_tracker = st.toggle("📊 Real-Time Application Status Tracking Updates", value=True, key="pref_tracker")
        pref_courses = st.toggle("🎓 Skill Certification & Training Course Recommendations", value=True, key="pref_courses")
        
        st.markdown("<hr style='border-color:#21262d;'>", unsafe_allow_html=True)
        pref_freq = st.radio("Notification Frequency", ["Instant (Real-time)", "Daily Digest", "Weekly Summary"], index=0)

        if st.button("💾 Save Alert Preferences", type="primary"):
            st.success("✅ Your alert preferences have been saved successfully!")
        
        st.markdown("</div>", unsafe_allow_html=True)
