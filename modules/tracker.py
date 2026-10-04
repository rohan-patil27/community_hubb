import streamlit as st
from modules.database import get_conn, send_sms
from datetime import datetime
import re

JOB_STATUS_STEPS = ["Applied", "Under Review", "Interview Scheduled", "Selected", "Rejected"]
SCHEME_STATUS_STEPS = ["Submitted", "Under Verification", "Approved", "Disbursed", "Rejected"]

STATUS_BADGES = {
    # Job Statuses
    "Applied": ("#1e3a5f", "#60a5fa", "#2d4a8a", "🔵"),
    "Under Review": ("#2d2000", "#fbbf24", "#78350f", "🟡"),
    "Interview Scheduled": ("#2d1b69", "#a78bfa", "#4c1d95", "🟣"),
    "Selected": ("#0d2d1a", "#34d399", "#065f46", "🟢"),
    
    # Scheme Statuses
    "Submitted": ("#1e3a5f", "#60a5fa", "#2d4a8a", "🔵"),
    "Under Verification": ("#2d2000", "#fbbf24", "#78350f", "🟡"),
    "Approved": ("#0d2d1a", "#34d399", "#065f46", "🟢"),
    "Approved / Sanctioned": ("#0d2d1a", "#34d399", "#065f46", "🟢"),
    "Disbursed": ("#064e3b", "#34d399", "#047857", "💸"),
    
    # Common
    "Rejected": ("#2d1515", "#f87171", "#7f1d1d", "❌"),
}

def mask_phone(phone_str):
    """Masks phone numbers for privacy e.g. 98******10"""
    if not phone_str:
        return "N/A"
    clean = re.sub(r'\D', '', str(phone_str))
    if len(clean) >= 10:
        return f"{clean[:2]}******{clean[-2:]}"
    elif len(clean) >= 6:
        return f"{clean[:2]}***{clean[-2:]}"
    return str(phone_str)


def map_scheme_status(status_str):
    """Maps legacy scheme status values to standard flow"""
    if status_str in ["Applied", "Submitted"]:
        return "Submitted"
    elif status_str in ["Under Review", "Under Verification"]:
        return "Under Verification"
    elif status_str in ["Approved / Sanctioned", "Approved"]:
        return "Approved"
    elif status_str == "Disbursed":
        return "Disbursed"
    elif status_str == "Rejected":
        return "Rejected"
    return "Submitted"


def delete_job_application(app_id):
    """Deletes job application record"""
    try:
        conn = get_conn()
        conn.execute("DELETE FROM applications WHERE id=?", (app_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Delete job app error:", e)
        return False


def delete_scheme_application(sch_app_id):
    """Deletes scheme application record"""
    try:
        conn = get_conn()
        conn.execute("DELETE FROM scheme_applications WHERE id=?", (sch_app_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Delete scheme app error:", e)
        return False


def show_tracker(user, t):
    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon">📊</div>
        <div>
            <h2>Application Status Tracker</h2>
            <p>Track job applications & government scheme submissions with visual status timelines</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["💼 Job Applications", "🏛️ Government Scheme Applications"])

    conn = get_conn()
    conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
    c = conn.cursor()

    # ==========================================
    # --- TAB 1: JOB APPLICATIONS TRACKER ---
    # ==========================================
    with tab1:
        c.execute("""
            SELECT a.id, j.title, j.company, j.location, j.salary_min, j.salary_max,
                   j.description as job_desc, a.status, a.applied_at, a.updated_at,
                   a.reminder_date, a.notes, j.contact, j.id as job_id
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            WHERE a.user_id = ?
            ORDER BY a.applied_at DESC
        """, (user['id'],))
        raw_job_apps = c.fetchall()

        if not raw_job_apps:
            st.markdown("""
            <div style="background:#161b22;border:1px solid #21262d;border-radius:12px;padding:2.5rem;text-align:center;margin:1.5rem 0;">
                <div style="font-size:2.5rem;margin-bottom:0.75rem;">📋</div>
                <div style="color:#e6edf3;font-size:1.1rem;font-weight:600;">No job applications tracked yet</div>
                <div style="color:#8b949e;font-size:0.88rem;margin-top:0.3rem;">Visit the AI Job Matching page to apply for openings!</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Summary Metrics Bar
            job_status_counts = {}
            for ja in raw_job_apps:
                job_status_counts[ja['status']] = job_status_counts.get(ja['status'], 0) + 1

            metric_cols = st.columns(5)
            for mcol, status_step in zip(metric_cols, JOB_STATUS_STEPS):
                cnt = job_status_counts.get(status_step, 0)
                bg, fg, border, icon = STATUS_BADGES.get(status_step, ("#161b22", "#e6edf3", "#21262d", "📋"))
                with mcol:
                    st.markdown(f"""
                    <div style="background:{bg};border:1px solid {border};border-radius:10px;padding:0.75rem;text-align:center;">
                        <div style="color:{fg};font-size:1.3rem;font-weight:700;">{cnt}</div>
                        <div style="color:{fg};font-size:0.75rem;font-weight:600;margin-top:2px;">{icon} {status_step}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Filter & Search Controls
            fcol1, fcol2, fcol3 = st.columns([1.5, 1.2, 1.3])
            with fcol1:
                job_search = st.text_input("🔍 Search Job Applications", placeholder="Search by job title, company, location...", key="job_app_search")
            with fcol2:
                job_status_filter = st.selectbox("📌 Status Filter", ["All"] + JOB_STATUS_STEPS, key="job_app_status_filter")
            with fcol3:
                job_date_sort = st.selectbox("📅 Date Order", ["Newest First", "Oldest First"], key="job_app_date_sort")

            filtered_job_apps = raw_job_apps
            if job_status_filter != "All":
                filtered_job_apps = [ja for ja in filtered_job_apps if ja['status'] == job_status_filter]

            if job_search:
                q = job_search.lower().strip()
                filtered_job_apps = [
                    ja for ja in filtered_job_apps
                    if q in ja['title'].lower() or q in ja['company'].lower() or q in ja['location'].lower() or q in ja.get('notes','').lower()
                ]

            if job_date_sort == "Oldest First":
                filtered_job_apps.reverse()

            st.markdown(f"<div style='color:#8b949e;font-size:0.85rem;margin-bottom:1rem;'>Showing <b style='color:#60a5fa;'>{len(filtered_job_apps)}</b> job applications</div>", unsafe_allow_html=True)

            # Render Job Application Cards
            for app in filtered_job_apps:
                ref_id = f"APP-JOB-{app['id']:04d}"
                status = app['status']
                bg, fg, border, icon = STATUS_BADGES.get(status, ("#161b22", "#e6edf3", "#21262d", "📋"))
                applied_date = app['applied_at'][:10] if app.get('applied_at') else "N/A"
                updated_raw = app.get('updated_at') or ""
                updated_date = updated_raw[:10] if (updated_raw and updated_raw >= applied_date) else applied_date
                masked_contact = mask_phone(app.get('contact', ''))

                # Timeline calculation
                cur_step_idx = JOB_STATUS_STEPS.index(status) if status in JOB_STATUS_STEPS else 0
                progress_pct = int(((cur_step_idx + 1) / len(JOB_STATUS_STEPS)) * 100)

                timeline_steps_html = ""
                for s_idx, s_name in enumerate(JOB_STATUS_STEPS):
                    if s_idx < cur_step_idx:
                        s_color = "#34d399"
                        s_label = f"✓ {s_name}"
                        s_date = applied_date if s_idx == 0 else updated_date
                        date_color = "#a7f3d0"
                    elif s_idx == cur_step_idx:
                        s_color = fg
                        s_label = f"<b>{s_name}</b>"
                        s_date = applied_date if s_idx == 0 else updated_date
                        date_color = "#60a5fa"
                    else:
                        s_color = "#8b949e"
                        s_label = s_name
                        s_date = "Pending"
                        date_color = "#64748b"

                    timeline_steps_html += f'<div style="flex:1;text-align:center;font-size:1.02rem;font-weight:700;color:{s_color};padding:0 4px;"><div>{s_label}</div><div style="font-size:0.88rem;color:{date_color};margin-top:4px;font-weight:600;">{s_date}</div></div>'

                card_html = (
                    f'<div style="background:#161b22;border:1px solid #21262d;border-left:5px solid {border};border-radius:14px;padding:1.35rem;margin-bottom:1.2rem;">'
                    f'<div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:0.75rem;margin-bottom:0.75rem;">'
                    f'<div>'
                    f'<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:4px;">'
                    f'<span style="background:#21262d;color:#a78bfa;border:1px solid #30363d;border-radius:6px;padding:2px 8px;font-size:0.82rem;font-weight:700;">🆔 {ref_id}</span>'
                    f'<span style="color:#94a3b8;font-size:0.85rem;font-weight:500;">📅 Applied: {applied_date}</span>'
                    f'</div>'
                    f'<div style="font-family:\'Sora\',sans-serif;font-weight:700;color:#e6edf3;font-size:1.2rem;">{app["title"]}</div>'
                    f'<div style="color:#60a5fa;font-size:0.95rem;font-weight:600;margin-top:2px;">🏢 {app["company"]} • 📍 {app["location"]}</div>'
                    f'</div>'
                    f'<div style="background:{bg};border:1.5px solid {border};border-radius:20px;padding:6px 16px;font-size:0.9rem;font-weight:700;color:{fg};">{icon} {status}</div>'
                    f'</div>'

                    f'<div style="display:flex;flex-wrap:wrap;gap:0.6rem;margin-bottom:0.85rem;">'
                    f'<span style="background:#0d2d1a;color:#34d399;border:1px solid #065f46;border-radius:6px;padding:4px 10px;font-size:0.85rem;font-weight:600;">💰 ₹{app["salary_min"]:,}–₹{app["salary_max"]:,}/mo</span>'
                    f'<span style="background:#1e3a5f;color:#60a5fa;border:1px solid #2d4a8a;border-radius:6px;padding:4px 10px;font-size:0.85rem;font-weight:600;">📞 HR Contact: {masked_contact}</span>'
                    f'<span style="background:#21262d;color:#94a3b8;border:1px solid #30363d;border-radius:6px;padding:4px 10px;font-size:0.85rem;font-weight:600;">🔄 Last Updated: {updated_date}</span>'
                    f'</div>'

                    # Visual Status Timeline Bar
                    f'<div style="background:#0d1117;border:1px solid #30363d;border-radius:12px;padding:1.1rem 0.85rem;margin:1rem 0;">'
                    f'<div style="display:flex;justify-content:space-between;margin-bottom:10px;">{timeline_steps_html}</div>'
                    f'<div style="background:#21262d;border-radius:6px;height:10px;overflow:hidden;">'
                    f'<div style="width:{progress_pct}%;height:100%;background:{fg};transition:width 0.5s;"></div>'
                    f'</div>'
                    f'</div>'
                    f'</div>'
                )

                st.markdown(card_html, unsafe_allow_html=True)

                # Action Controls Row
                col_act1, col_act2, col_act3, col_act4 = st.columns([1, 1.2, 1, 0.8])

                with col_act1:
                    with st.expander("ℹ️ View Details"):
                        st.markdown(f"""
                        <div style="font-size:0.82rem;color:#e6edf3;line-height:1.5;">
                            <div style="margin-bottom:0.4rem;"><b style="color:#60a5fa;">📋 Job Description:</b><br>{app.get('job_desc','N/A')}</div>
                            <div style="margin-bottom:0.4rem;"><b style="color:#60a5fa;">📝 My Application Notes:</b><br>{app.get('notes','No custom notes added.')}</div>
                            <div style="margin-bottom:0.4rem;"><b style="color:#60a5fa;">⏰ Follow-up Reminder:</b> {app.get('reminder_date','None set')}</div>
                        </div>
                        """, unsafe_allow_html=True)

                with col_act2:
                    with st.expander("✏️ Update Status / Notes"):
                        cur_status_idx = JOB_STATUS_STEPS.index(status) if status in JOB_STATUS_STEPS else 0
                        new_job_status = st.selectbox("Update Status", JOB_STATUS_STEPS, index=cur_status_idx, key=f"job_st_sel_{app['id']}")
                        new_job_notes = st.text_area("Notes (interview date, interviewer name, follow-up...)", value=app.get('notes','') or '', key=f"job_notes_{app['id']}", height=70)
                        new_reminder = st.text_input("⏰ Set Reminder (e.g. 10 Oct at 11 AM)", value=app.get('reminder_date','') or '', key=f"job_rem_{app['id']}")

                        if st.button("💾 Save Changes & Alert", key=f"save_job_app_{app['id']}", type="primary", use_container_width=True):
                            cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            conn.execute("UPDATE applications SET status=?, notes=?, reminder_date=?, updated_at=? WHERE id=?",
                                         (new_job_status, new_job_notes, new_reminder, cur_time, app['id']))
                            conn.commit()

                            sms_msg = f"📱 Smart Slum Alert: Your Job application for '{app['title']}' at '{app['company']}' status updated to '{new_job_status}'."
                            send_sms(user['phone'], sms_msg, sms_type="Job Tracker Update", user_id=user['id'])

                            st.toast("✅ Saved & SMS alert sent!", icon="💬")
                            st.rerun()

                with col_act3:
                    if st.button(f"🌐 Open Job Details", key=f"open_job_{app['id']}", use_container_width=True):
                        st.session_state.page = 'jobs'
                        st.rerun()

                with col_act4:
                    if st.button(f"🗑️ Delete", key=f"del_job_app_{app['id']}", use_container_width=True):
                        if delete_job_application(app['id']):
                            st.toast("🗑️ Application removed!", icon="✅")
                            st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)

    # ===================================================
    # --- TAB 2: GOVERNMENT SCHEME APPLICATIONS TRACKER ---
    # ===================================================
    with tab2:
        c.execute("""
            SELECT sa.id, s.name as scheme_name, s.category, s.benefits, s.apply_link, s.helpline,
                   sa.status, sa.applied_at, sa.updated_at, sa.reminder_date, sa.notes, s.id as scheme_id
            FROM scheme_applications sa
            JOIN schemes s ON sa.scheme_id = s.id
            WHERE sa.user_id = ?
            ORDER BY sa.applied_at DESC
        """, (user['id'],))
        raw_sch_apps = c.fetchall()

        if not raw_sch_apps:
            st.markdown("""
            <div style="background:#161b22;border:1px solid #21262d;border-radius:12px;padding:2.5rem;text-align:center;margin:1.5rem 0;">
                <div style="font-size:2.5rem;margin-bottom:0.75rem;">🏛️</div>
                <div style="color:#e6edf3;font-size:1.1rem;font-weight:600;">No government scheme applications tracked yet</div>
                <div style="color:#8b949e;font-size:0.88rem;margin-top:0.3rem;">Visit the Government Scheme Finder and click 'Apply Online' to track schemes!</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Metric Bar for Schemes
            sch_status_counts = {}
            for sa in raw_sch_apps:
                mapped_st = map_scheme_status(sa['status'])
                sch_status_counts[mapped_st] = sch_status_counts.get(mapped_st, 0) + 1

            sch_metric_cols = st.columns(5)
            for mcol, status_step in zip(sch_metric_cols, SCHEME_STATUS_STEPS):
                cnt = sch_status_counts.get(status_step, 0)
                bg, fg, border, icon = STATUS_BADGES.get(status_step, ("#161b22", "#e6edf3", "#21262d", "🏛️"))
                with mcol:
                    st.markdown(f"""
                    <div style="background:{bg};border:1px solid {border};border-radius:10px;padding:0.75rem;text-align:center;">
                        <div style="color:{fg};font-size:1.3rem;font-weight:700;">{cnt}</div>
                        <div style="color:{fg};font-size:0.75rem;font-weight:600;margin-top:2px;">{icon} {status_step}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Filter & Search Controls for Schemes
            scol1, scol2, scol3 = st.columns([1.5, 1.2, 1.3])
            with scol1:
                sch_search = st.text_input("🔍 Search Scheme Applications", placeholder="Search by scheme name, category...", key="sch_app_search")
            with scol2:
                sch_status_filter = st.selectbox("📌 Scheme Status Filter", ["All"] + SCHEME_STATUS_STEPS, key="sch_app_status_filter")
            with scol3:
                sch_date_sort = st.selectbox("📅 Date Order", ["Newest First", "Oldest First"], key="sch_app_date_sort")

            filtered_sch_apps = raw_sch_apps
            if sch_status_filter != "All":
                filtered_sch_apps = [sa for sa in filtered_sch_apps if map_scheme_status(sa['status']) == sch_status_filter]

            if sch_search:
                q = sch_search.lower().strip()
                filtered_sch_apps = [
                    sa for sa in filtered_sch_apps
                    if q in sa['scheme_name'].lower() or q in sa['category'].lower() or q in sa.get('notes','').lower()
                ]

            if sch_date_sort == "Oldest First":
                filtered_sch_apps.reverse()

            st.markdown(f"<div style='color:#8b949e;font-size:0.85rem;margin-bottom:1rem;'>Showing <b style='color:#34d399;'>{len(filtered_sch_apps)}</b> scheme applications</div>", unsafe_allow_html=True)

            # Render Scheme Application Cards
            for sch_app in filtered_sch_apps:
                ref_id = f"APP-SCH-{sch_app['id']:04d}"
                mapped_status = map_scheme_status(sch_app['status'])
                bg, fg, border, icon = STATUS_BADGES.get(mapped_status, ("#161b22", "#e6edf3", "#21262d", "🏛️"))
                applied_date = sch_app['applied_at'][:10] if sch_app.get('applied_at') else "N/A"
                updated_raw = sch_app.get('updated_at') or ""
                updated_date = updated_raw[:10] if (updated_raw and updated_raw >= applied_date) else applied_date

                # Scheme Timeline calculation
                cur_step_idx = SCHEME_STATUS_STEPS.index(mapped_status) if mapped_status in SCHEME_STATUS_STEPS else 0
                progress_pct = int(((cur_step_idx + 1) / len(SCHEME_STATUS_STEPS)) * 100)

                timeline_steps_html = ""
                for s_idx, s_name in enumerate(SCHEME_STATUS_STEPS):
                    if s_idx < cur_step_idx:
                        s_color = "#34d399"
                        s_label = f"✓ {s_name}"
                        s_date = applied_date if s_idx == 0 else updated_date
                        date_color = "#a7f3d0"
                    elif s_idx == cur_step_idx:
                        s_color = fg
                        s_label = f"<b>{s_name}</b>"
                        s_date = applied_date if s_idx == 0 else updated_date
                        date_color = "#60a5fa"
                    else:
                        s_color = "#8b949e"
                        s_label = s_name
                        s_date = "Pending"
                        date_color = "#64748b"

                    timeline_steps_html += f'<div style="flex:1;text-align:center;font-size:1.02rem;font-weight:700;color:{s_color};padding:0 4px;"><div>{s_label}</div><div style="font-size:0.88rem;color:{date_color};margin-top:4px;font-weight:600;">{s_date}</div></div>'

                card_html = (
                    f'<div style="background:#161b22;border:1px solid #21262d;border-left:5px solid {border};border-radius:14px;padding:1.35rem;margin-bottom:1.2rem;">'
                    f'<div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:0.75rem;margin-bottom:0.75rem;">'
                    f'<div>'
                    f'<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:4px;">'
                    f'<span style="background:#21262d;color:#34d399;border:1px solid #30363d;border-radius:6px;padding:2px 8px;font-size:0.82rem;font-weight:700;">🆔 {ref_id}</span>'
                    f'<span style="color:#94a3b8;font-size:0.85rem;font-weight:500;">📅 Submitted: {applied_date}</span>'
                    f'</div>'
                    f'<div style="font-family:\'Sora\',sans-serif;font-weight:700;color:#e6edf3;font-size:1.2rem;">🏛️ {sch_app["scheme_name"]}</div>'
                    f'<div style="color:#60a5fa;font-size:0.95rem;font-weight:600;margin-top:2px;">📂 Category: {sch_app["category"]}</div>'
                    f'</div>'
                    f'<div style="background:{bg};border:1.5px solid {border};border-radius:20px;padding:6px 16px;font-size:0.9rem;font-weight:700;color:{fg};">{icon} {mapped_status}</div>'
                    f'</div>'

                    f'<div style="background:#0d1117;border:1px solid #21262d;border-radius:8px;padding:0.75rem 1rem;margin-bottom:0.85rem;color:#34d399;font-weight:600;font-size:0.92rem;">'
                    f'🎁 <b>Benefits:</b> {sch_app["benefits"]}'
                    f'</div>'

                    f'<div style="display:flex;flex-wrap:wrap;gap:0.6rem;margin-bottom:0.85rem;">'
                    f'<span style="background:#1e3a5f;color:#60a5fa;border:1px solid #2d4a8a;border-radius:6px;padding:4px 10px;font-size:0.85rem;font-weight:600;">📞 Helpline: {sch_app.get("helpline","1800-11-0001")}</span>'
                    f'<span style="background:#21262d;color:#94a3b8;border:1px solid #30363d;border-radius:6px;padding:4px 10px;font-size:0.85rem;font-weight:600;">🔄 Last Updated: {updated_date}</span>'
                    f'</div>'

                    # Visual Scheme Status Timeline
                    f'<div style="background:#0d1117;border:1px solid #30363d;border-radius:12px;padding:1.1rem 0.85rem;margin:1rem 0;">'
                    f'<div style="display:flex;justify-content:space-between;margin-bottom:10px;">{timeline_steps_html}</div>'
                    f'<div style="background:#21262d;border-radius:6px;height:10px;overflow:hidden;">'
                    f'<div style="width:{progress_pct}%;height:100%;background:{fg};transition:width 0.5s;"></div>'
                    f'</div>'
                    f'</div>'
                    f'</div>'
                )

                st.markdown(card_html, unsafe_allow_html=True)

                # Action Controls Row for Scheme
                scol_act1, scol_act2, scol_act3, scol_act4 = st.columns([1, 1.2, 1, 0.8])

                with scol_act1:
                    with st.expander("ℹ️ View Details"):
                        st.markdown(f"""
                        <div style="font-size:0.82rem;color:#e6edf3;line-height:1.5;">
                            <div style="margin-bottom:0.4rem;"><b style="color:#60a5fa;">🎁 Scheme Benefits:</b> {sch_app['benefits']}</div>
                            <div style="margin-bottom:0.4rem;"><b style="color:#60a5fa;">📝 My Scheme Notes / Ref No:</b><br>{sch_app.get('notes','No notes added.')}</div>
                            <div style="margin-bottom:0.4rem;"><b style="color:#60a5fa;">⏰ Follow-up Reminder:</b> {sch_app.get('reminder_date','None set')}</div>
                        </div>
                        """, unsafe_allow_html=True)

                with scol_act2:
                    with st.expander("✏️ Update Status / Notes"):
                        cur_sch_status_idx = SCHEME_STATUS_STEPS.index(mapped_status) if mapped_status in SCHEME_STATUS_STEPS else 0
                        new_sch_status = st.selectbox("Update Status", SCHEME_STATUS_STEPS, index=cur_sch_status_idx, key=f"sch_st_sel_{sch_app['id']}")
                        new_sch_notes = st.text_area("Notes (Reference number, token no, document verification...)", value=sch_app.get('notes','') or '', key=f"sch_notes_{sch_app['id']}", height=70)
                        new_sch_reminder = st.text_input("⏰ Set Reminder (e.g. 15 Oct Verification)", value=sch_app.get('reminder_date','') or '', key=f"sch_rem_{sch_app['id']}")

                        if st.button("💾 Save Scheme Status", key=f"save_sch_app_{sch_app['id']}", type="primary", use_container_width=True):
                            cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            conn.execute("UPDATE scheme_applications SET status=?, notes=?, reminder_date=?, updated_at=? WHERE id=?",
                                         (new_sch_status, new_sch_notes, new_sch_reminder, cur_time, sch_app['id']))
                            conn.commit()

                            sms_msg = f"📱 Smart Slum Alert: Your Scheme application for '{sch_app['scheme_name']}' status updated to '{new_sch_status}'."
                            send_sms(user['phone'], sms_msg, sms_type="Scheme Tracker Update", user_id=user['id'])

                            st.toast("✅ Scheme Application status updated!", icon="🏛️")
                            st.rerun()

                with scol_act3:
                    if st.button(f"🌐 Open Portal Link", key=f"open_sch_{sch_app['id']}", use_container_width=True):
                        st.markdown(f"<script>window.open('{sch_app.get('apply_link','https://mahadbt.maharashtra.gov.in')}','_blank')</script>", unsafe_allow_html=True)
                        st.info(f"🔗 Portal: {sch_app.get('apply_link','https://mahadbt.maharashtra.gov.in')}")

                with scol_act4:
                    if st.button(f"🗑️ Delete", key=f"del_sch_app_{sch_app['id']}", use_container_width=True):
                        if delete_scheme_application(sch_app['id']):
                            st.toast("🗑️ Scheme Application removed!", icon="✅")
                            st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)

    # ===================================================
    # --- 📱 RECEIVED SMS INBOX & ALERTS HISTORY ---
    # ===================================================
    st.markdown("<br><hr style='border-color:#21262d;'>", unsafe_allow_html=True)
    with st.expander("📱 Received SMS Inbox & Application Alerts History", expanded=True):
        c.execute("""
            SELECT * FROM sms_logs 
            WHERE phone=? OR user_id=? 
            ORDER BY created_at DESC
        """, (user['phone'], user['id']))
        sms_list = c.fetchall()

        if not sms_list:
            st.info("No SMS notifications received yet.")
        else:
            st.markdown(f"<div style='color:#8b949e;font-size:0.85rem;margin-bottom:0.8rem;'>Delivered to <b style='color:#60a5fa;'>{mask_phone(user['phone'])}</b> ({len(sms_list)} messages)</div>", unsafe_allow_html=True)
            for sms in sms_list:
                time_str = sms['created_at'][:19] if sms.get('created_at') else "Just now"
                st.markdown(f"""
                <div style="background:#161b22;border:1px solid #30363d;border-radius:10px;padding:0.85rem 1.2rem;margin-bottom:0.6rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-weight:700;color:#34d399;font-size:0.85rem;">📱 {sms['sms_type']} SMS</span>
                        <span style="color:#8b949e;font-size:0.75rem;">🕒 {time_str}</span>
                    </div>
                    <div style="font-family:monospace;font-size:0.9rem;color:#e6edf3;margin-top:0.4rem;background:#0d1117;padding:0.6rem 0.8rem;border-radius:6px;border:1px solid #21262d;">
                        "{sms['message']}"
                    </div>
                </div>
                """, unsafe_allow_html=True)

    conn.close()
