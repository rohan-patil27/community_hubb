import streamlit as st
import urllib.parse
from datetime import datetime
from modules.database import get_conn

def show_resume_generator(user, t):
    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon">📄</div>
        <div>
            <h2>Professional Resume Builder</h2>
            <p>Create ATS-friendly, professional resumes with clean layout, standard section ordering, and instant PDF download</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize Session States for Resume Form if not present
    if 'res_template' not in st.session_state: st.session_state.res_template = "Modern Clean"

    col_form, col_preview = st.columns([1, 1.1])

    with col_form:
        st.markdown("""<div style="background:#161b22;border:1px solid #21262d;border-radius:14px;padding:1.5rem;margin-bottom:1rem;">
        <div style="font-weight:700;color:#e6edf3;font-size:1.1rem;margin-bottom:1rem;">🎨 Choose Resume Theme</div>""", unsafe_allow_html=True)
        
        template = st.selectbox(
            "Select Design Theme",
            ["Modern Clean", "Executive Corporate", "Classic Minimal"],
            key="resume_theme_select"
        )
        st.session_state.res_template = template

        st.markdown("<hr style='border-color:#21262d;'>", unsafe_allow_html=True)
        st.markdown("""<div style="font-weight:700;color:#e6edf3;font-size:1.1rem;margin-bottom:1rem;">✏️ Resume Information</div>""", unsafe_allow_html=True)

        # 1. Header (Name, Title, Contact, Links)
        with st.expander("👤 Header & Contact Info", expanded=True):
            name = st.text_input("Full Name *", value=user.get('name','John Doe'), key="rb_name")
            title = st.text_input("Professional Title", value=user.get('skills','Data Engineer').split(',')[0].title(), placeholder="e.g. Data Engineer / Full Stack Developer", key="rb_title")
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                phone = st.text_input("Phone *", value=user.get('phone','+91 9876543210'), key="rb_phone")
            with col_c2:
                email = st.text_input("Email", value="user@example.com", key="rb_email")
            with col_c3:
                location = st.text_input("Location *", value=f"{user.get('location','Jalgaon')}, Maharashtra", key="rb_loc")
            
            col_l1, col_l2, col_l3 = st.columns(3)
            with col_l1:
                linkedin = st.text_input("LinkedIn Profile", value="linkedin.com/in/profile", key="rb_linkedin")
            with col_l2:
                github = st.text_input("GitHub Profile", value="github.com/username", key="rb_github")
            with col_l3:
                portfolio = st.text_input("Portfolio / Website", value="portfolio.me", key="rb_portfolio")

        # 2. Professional Summary
        with st.expander("📝 1. Professional Summary", expanded=False):
            summary = st.text_area(
                "Professional Summary",
                value=f"Results-driven {title} with strong technical competencies and hands-on experience in problem solving, system optimization, and collaboration. Passionate about leveraging technology to build scalable, high-quality solutions.",
                height=90,
                key="rb_summary"
            )

        # 3. Technical Skills
        with st.expander("🧠 2. Technical Skills", expanded=False):
            skills = st.text_area(
                "Technical Skills (Languages, Frameworks, Tools, Databases)",
                value=user.get('skills','Python, SQL, Data Engineering, Streamlit, Git, Docker, PostgreSQL'),
                height=70,
                key="rb_skills"
            )

        # 4. Education
        with st.expander("🎓 3. Education", expanded=False):
            edu_degree = st.text_input("Degree / Qualification", value=user.get('education','B.Tech in Computer Science & Engineering'), key="rb_edu_deg")
            edu_school = st.text_input("University / Institution", value="Government Engineering College / University of Technology", key="rb_edu_school")
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                edu_year = st.text_input("Year / Duration", value="2020 – 2024", key="rb_edu_year")
            with col_e2:
                edu_grade = st.text_input("CGPA / Grade", value="8.6 / 10.0", key="rb_edu_grade")

        # 5. Projects
        with st.expander("🚀 4. Projects", expanded=False):
            proj_title = st.text_input("Project Name & Tech Stack", value="Community Hub & Resource Portal (Python, Streamlit, SQLite)", key="rb_proj_name")
            proj_desc = st.text_area("Key Details & Achievements", value="• Developed a centralized multi-service digital platform for municipal services, job placement, and emergency support.\n• Integrated interactive maps, password validation, and dynamic analytics serving 1,000+ local residents.", height=90, key="rb_proj_desc")

        # 6. Experience / Internship
        with st.expander("💼 5. Experience / Internship", expanded=False):
            exp_role = st.text_input("Role & Designation", value=f"Junior {title} / Intern", key="rb_exp_role")
            exp_company = st.text_input("Company / Organization", value="Tech Innovations Solutions", key="rb_exp_comp")
            exp_duration = st.text_input("Duration", value="Jan 2024 – Present", key="rb_exp_dur")
            exp_details = st.text_area("Responsibilities & Key Deliverables", value="• Designed and automated ETL data pipelines reducing query latency by 35%.\n• Built interactive dashboards and collaborated with cross-functional engineering teams.", height=90, key="rb_exp_det")

        # 7. Certifications
        with st.expander("🏅 6. Certifications", expanded=False):
            cert_details = st.text_area("Certifications (one per line)", value="• AWS Certified Cloud Practitioner (2024)\n• Google Data Analytics Professional Certificate", height=70, key="rb_certs")

        # 8. Achievements
        with st.expander("🏆 7. Achievements", expanded=False):
            achievements = st.text_area("Achievements & Awards", value="• Secured 1st Rank in Annual Hackathon for Smart City Solutions.\n• Published Research Paper on Efficient Data Pipeline Optimization.", height=70, key="rb_achievements")

        # 9. Languages
        with st.expander("🌐 8. Languages", expanded=False):
            languages = st.text_input("Languages Known", value="English | Hindi | Marathi", key="rb_lang")

        # 10. Declaration
        with st.expander("📋 9. Declaration & Place", expanded=False):
            place = st.text_input("Place / City", value=user.get('district','Jalgaon'), key="rb_place")
            include_decl = st.checkbox("Include Signed Declaration Section", value=True, key="rb_decl_check")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_preview:
        st.markdown(f"""<div style="background:#161b22;border:1px solid #21262d;border-radius:14px;padding:1.5rem;position:sticky;top:20px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
            <div style="font-weight:700;color:#e6edf3;font-size:1.1rem;">👁️ Live Resume Preview</div>
        </div>""", unsafe_allow_html=True)

        # Generate HTML content for preview
        resume_html = _build_resume_html(
            template=template,
            name=name, title=title, phone=phone, email=email, location=location,
            linkedin=linkedin, github=github, portfolio=portfolio,
            summary=summary, skills=skills,
            edu_degree=edu_degree, edu_school=edu_school, edu_year=edu_year, edu_grade=edu_grade,
            proj_title=proj_title, proj_desc=proj_desc,
            exp_role=exp_role, exp_company=exp_company, exp_duration=exp_duration, exp_details=exp_details,
            cert_details=cert_details, achievements=achievements, languages=languages,
            place=place, include_decl=include_decl
        )

        st.components.v1.html(resume_html, height=750, scrolling=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
    with col_d2:
        st.markdown("""
        <style>
        div[data-testid="stDownloadButton"] > button {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #1d4ed8 100%) !important;
            color: #ffffff !important;
            border: 1px solid #3b82f6 !important;
            border-radius: 12px !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 700 !important;
            font-size: 1.05rem !important;
            box-shadow: 0 4px 15px rgba(30, 58, 138, 0.4) !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stDownloadButton"] > button:hover {
            background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 100%) !important;
            border-color: #60a5fa !important;
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5) !important;
            transform: translateY(-2px) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        file_name = f"Resume_{name.replace(' ','_') if name else 'User'}.html"
        st.download_button(
            label="📥 Download Resume (HTML/PDF)",
            data=resume_html,
            file_name=file_name,
            mime="text/html",
            type="primary",
            use_container_width=True,
            key="dl_pro_resume"
        )
        st.info("💡 **Convert to PDF:** Open downloaded file in Chrome/Edge browser -> Press `Ctrl + P` -> Select **Save as PDF**!")


def _build_resume_html(template, name, title, phone, email, location, linkedin, github, portfolio, summary, skills, edu_degree, edu_school, edu_year, edu_grade, proj_title, proj_desc, exp_role, exp_company, exp_duration, exp_details, cert_details, achievements, languages, place="Jalgaon", include_decl=True):
    date_today = datetime.now().strftime("%d %B %Y")

    # Format bullets
    def format_bullets(text):
        if not text: return ""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return "".join([f"<li>{l.lstrip('•- ')}</li>" for l in lines])

    exp_bullets = format_bullets(exp_details)
    proj_bullets = format_bullets(proj_desc)
    cert_bullets = format_bullets(cert_details)
    ach_bullets = format_bullets(achievements)

    # Format skills line-by-line
    skills_formatted = "<br>".join([s.strip() for s in skills.split('\n') if s.strip()]) if skills else ""

    # Header Contact bar line: Phone | Email | Location
    contacts_list = [c for c in [phone, email, location] if c.strip()]
    contacts_str = " | ".join(contacts_list)

    # Links bar line: LinkedIn | GitHub | Portfolio
    links_list = [l for l in [linkedin, github, portfolio] if l.strip()]
    links_str = " | ".join(links_list)

    # Color & Theme Configurations
    if template == "Executive Corporate":
        font_family = "'Plus Jakarta Sans', -apple-system, sans-serif"
        header_box_style = "background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%); color: #ffffff; padding: 1.8rem 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; text-align: center; border: 1px solid #1e40af; box-shadow: 0 4px 15px rgba(30,58,138,0.15);"
        name_color = "#ffffff"
        name_size = "2.4rem"
        title_color = "#93c5fd"
        contact_color = "#e2e8f0"
        link_color = "#60a5fa"
        section_title_css = "font-size: 1.05rem; font-weight: 800; color: #1e3a8a; text-transform: uppercase; letter-spacing: 1px; border-left: 5px solid #2563eb; padding-left: 10px; background: #f8fafc; padding-top: 5px; padding-bottom: 5px; margin-bottom: 0.75rem; border-radius: 0 6px 6px 0;"
        divider_css = "border: none; border-top: 1px solid #e2e8f0; margin: 1.2rem 0;"
        role_color = "#1e3a8a"
    elif template == "Classic Minimal":
        font_family = "'Georgia', 'Times New Roman', serif"
        header_box_style = "text-align: center; border-top: 3px double #581c87; border-bottom: 1px solid #581c87; padding: 1.2rem 0; margin-bottom: 1.5rem;"
        name_color = "#581c87"
        name_size = "2.3rem"
        title_color = "#7e22ce"
        contact_color = "#4b5563"
        link_color = "#6b21a8"
        section_title_css = "font-size: 1.05rem; font-weight: 700; color: #581c87; font-variant: small-caps; letter-spacing: 1.2px; border-bottom: 1.5px dashed #a855f7; padding-bottom: 0.3rem; margin-bottom: 0.65rem;"
        divider_css = "border: none; border-top: 1px dashed #e9d5ff; margin: 1.2rem 0;"
        role_color = "#3b0764"
    else: # Modern Clean
        font_family = "'Inter', -apple-system, sans-serif"
        header_box_style = "text-align: center; margin-bottom: 1rem;"
        name_color = "#0f172a"
        name_size = "2.2rem"
        title_color = "#475569"
        contact_color = "#334155"
        link_color = "#2563eb"
        section_title_css = "font-size: 1rem; font-weight: 800; color: #0f172a; text-transform: uppercase; letter-spacing: 0.8px; border-bottom: 2px solid #0f172a; padding-bottom: 0.3rem; margin-bottom: 0.5rem;"
        divider_css = "border: none; border-top: 1.5px solid #000000; margin: 1.2rem 0;"
        role_color = "#0f172a"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Resume - {name}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: {font_family};
    color: #1e293b;
    background: #ffffff;
    padding: 2.5rem;
    max-width: 850px;
    margin: 0 auto;
    line-height: 1.5;
  }}
  
  .header {{
    {header_box_style}
  }}
  .name {{
    font-size: {name_size};
    font-weight: 800;
    color: {name_color};
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 0.15rem;
  }}
  .title {{
    font-size: 1.05rem;
    font-weight: 600;
    color: {title_color};
    margin-bottom: 0.5rem;
  }}
  .contact-line {{
    font-size: 0.9rem;
    color: {contact_color};
    margin-bottom: 0.25rem;
  }}
  .links-line {{
    font-size: 0.9rem;
    color: {link_color};
  }}
  .links-line a {{
    color: {link_color};
    text-decoration: none;
  }}

  .divider {{
    {divider_css}
  }}

  .section {{
    margin-bottom: 1.2rem;
  }}
  .section-title {{
    {section_title_css}
  }}

  .content-text {{
    font-size: 0.92rem;
    color: #334155;
    line-height: 1.6;
  }}

  .item-head {{
    display: flex;
    justify-content: space-between;
    font-weight: 700;
    font-size: 0.94rem;
    color: {role_color};
  }}
  .item-sub {{
    font-size: 0.88rem;
    color: #475569;
    font-weight: 600;
    margin-bottom: 0.3rem;
  }}

  ul {{
    padding-left: 1.2rem;
    font-size: 0.9rem;
    color: #334155;
    margin-top: 0.25rem;
  }}
  li {{
    margin-bottom: 0.25rem;
  }}

  @media print {{
    body {{ padding: 0; max-width: 100%; }}
    .section {{ page-break-inside: avoid; }}
    .divider {{ margin: 1rem 0; }}
  }}
</style>
</head>
<body>

  <!-- HEADER -->
  <div class="header">
    <div class="name">{name if name else 'NAME'}</div>
    <div class="title">{title if title else 'Professional Title'}</div>
    <div class="contact-line">{contacts_str if contacts_str else 'Phone | Email | Location'}</div>
    <div class="links-line">{links_str if links_str else 'LinkedIn | GitHub | Portfolio'}</div>
  </div>

  {'<hr class="divider">' if template != "Executive Corporate" else ''}

  <!-- PROFESSIONAL SUMMARY -->
  {f'''
  <div class="section">
    <div class="section-title">PROFESSIONAL SUMMARY</div>
    <div class="content-text">{summary}</div>
  </div>
  <hr class="divider">
  ''' if summary else ''}

  <!-- TECHNICAL SKILLS -->
  {f'''
  <div class="section">
    <div class="section-title">TECHNICAL SKILLS</div>
    <div class="content-text">{skills_formatted}</div>
  </div>
  <hr class="divider">
  ''' if skills_formatted else ''}

  <!-- EDUCATION -->
  {f'''
  <div class="section">
    <div class="section-title">EDUCATION</div>
    <div class="item-head">
      <span>{edu_degree}</span>
      <span>{edu_year}</span>
    </div>
    <div class="item-sub">{edu_school} {f'| Grade: {edu_grade}' if edu_grade else ''}</div>
  </div>
  <hr class="divider">
  ''' if edu_degree or edu_school else ''}

  <!-- PROJECTS -->
  {f'''
  <div class="section">
    <div class="section-title">PROJECTS</div>
    <div class="item-head">
      <span>{proj_title}</span>
    </div>
    {f'<ul>{proj_bullets}</ul>' if proj_bullets else f'<div class="content-text">{proj_desc}</div>'}
  </div>
  <hr class="divider">
  ''' if proj_title else ''}

  <!-- EXPERIENCE / INTERNSHIP -->
  {f'''
  <div class="section">
    <div class="section-title">EXPERIENCE / INTERNSHIP</div>
    <div class="item-head">
      <span>{exp_role}</span>
      <span>{exp_duration}</span>
    </div>
    <div class="item-sub">{exp_company}</div>
    {f'<ul>{exp_bullets}</ul>' if exp_bullets else f'<div class="content-text">{exp_details}</div>'}
  </div>
  <hr class="divider">
  ''' if exp_role or exp_company else ''}

  <!-- CERTIFICATIONS -->
  {f'''
  <div class="section">
    <div class="section-title">CERTIFICATIONS</div>
    {f'<ul>{cert_bullets}</ul>' if cert_bullets else f'<div class="content-text">{cert_details}</div>'}
  </div>
  <hr class="divider">
  ''' if cert_details else ''}

  <!-- ACHIEVEMENTS -->
  {f'''
  <div class="section">
    <div class="section-title">ACHIEVEMENTS</div>
    {f'<ul>{ach_bullets}</ul>' if ach_bullets else f'<div class="content-text">{achievements}</div>'}
  </div>
  <hr class="divider">
  ''' if achievements else ''}

  <!-- LANGUAGES -->
  {f'''
  <div class="section">
    <div class="section-title">LANGUAGES</div>
    <div class="content-text">{languages}</div>
  </div>
  ''' if languages else ''}

  <!-- DECLARATION -->
  {f'''
  <hr class="divider">
  <div class="section">
    <div class="section-title">DECLARATION</div>
    <div class="content-text">I hereby declare that all the details provided above are true, complete, and correct to the best of my knowledge and belief.</div>
    <div style="display: flex; justify-content: space-between; margin-top: 1.5rem; font-size: 0.9rem; color: #334155; font-weight: 600;">
      <div>
        <div>Place: {place}</div>
        <div>Date: {date_today}</div>
      </div>
      <div style="text-align: right;">
        <div>({name})</div>
        <div style="font-weight: 400; font-size: 0.85rem; color: #64748b;">Signature</div>
      </div>
    </div>
  </div>
  ''' if include_decl else ''}

</body>
</html>"""

