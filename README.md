# 🌟 Community Hub

> **Empowering underprivileged and urban communities with Jobs, Government Schemes, Skill Development, and AI-Powered Support.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 📖 Overview

**Community Hub** is a full-featured, AI-driven socio-economic platform designed specifically to bridge the opportunity gap for urban and underprivileged communities. By bringing jobs, verified government welfare schemes, free skill development courses, emergency helplines, and an intelligent multilingual voice assistant into a single accessible portal, Community Hub makes vital resources accessible even to users with low digital literacy.

---

## ✨ Key Features

### 🎙️ 1. AI Voice Assistant & Chatbot (Google Gemini + gTTS)
- **Voice-Enabled AI Assistance:** Powered by **Google Gemini AI** and **Google Text-to-Speech (gTTS)** to read answers aloud in regional languages.
- **Multilingual Understanding:** Responds naturally in the exact language the user speaks (Hindi, Marathi, English, etc.).
- **Persistent Key Storage:** Securely and permanently saves your Gemini API key in local settings.

### 💼 2. AI Skill-Based Job Matching & Skill Gap Analysis
- **Smart Match Scoring:** Uses Jaccard similarity and skill overlap algorithms to match candidates with suitable informal & formal jobs.
- **Skill Gap Analyzer:** Pinpoints exactly which skills are missing for a dream job and suggests tailored free training courses to bridge the gap.
- **Direct Apply:** One-click job application with instant status updates.

### 🏛️ 3. Government Scheme Eligibility Engine
- **Automated Eligibility Filter:** Matches users with local & central welfare schemes based on age, caste, gender, income, and district.
- **Scheme Tracker:** Track application progress from submission to disbursement.

### 📄 4. Instant 1-Click Resume Generator
- Generates clean, professional resumes instantly from user profile data.
- Downloadable in **HTML** and printable to **PDF** format.

### 📚 5. Free Skill Development & Courses
- Curated repository of verified free certifications, technical skills, vocational training, and government-backed courses (PMKVY, Swayam, etc.).

### 📋 6. Application Tracker
- Centralized tracking dashboard for all submitted job and scheme applications (*Applied, Shortlisted, Interviewing, Accepted, Rejected*).

### 🆘 7. Emergency Help & NGO Directory
- Directory of verified local NGOs, public hospitals, community shelters, and 24/7 national helplines.
- Location-based filtering across Indian states and districts.

### 🌐 8. 12+ Indian Regional Languages
- Complete UI translation support for **Hindi, Marathi, Gujarati, Punjabi, Bengali, Tamil, Telugu, Urdu, Kannada, Malayalam, Sanskrit, Sindhi, and English**.

### 🛡️ 9. Comprehensive Admin Dashboard
- **Analytics & Visual Charts:** Real-time metrics on user demographics, top in-demand skills, district-wise distribution, and job placements.
- **Content Moderation:** Approve, edit, or deactivate job postings and scheme listings.
- **Audit Logs:** Full logging of all admin actions for transparency and security.

---

## 🔐 Demo Credentials

| Role | Mobile / Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **🛡️ Admin** | `9999999999` | `admin123` | Full access to Admin Panel, moderation & analytics |
| **👤 User** | `9876543210` | `pass123` | Standard resident account |

---

## 🏗️ Tech Stack

- **Frontend & UI Framework:** [Streamlit](https://streamlit.io/) (Custom Dark Theme, Glassmorphic CSS, Responsive Layout)
- **AI & LLM Engine:** [Google Gemini Generative AI](https://ai.google.dev/) (`google-generativeai`)
- **Voice / TTS:** [gTTS](https://pypi.org/project/gTTS/) (Google Text-to-Speech)
- **Database:** SQLite3 (`slum_system.db`) with auto-migration and persistence
- **Data Processing:** Pandas
- **Language:** Python 3.8+

---

## 📁 Project Structure

```text
community_hub/
├── app.py                      # Main Streamlit application & navigation router
├── requirements.txt            # Python dependencies
├── slum_system.db              # SQLite persistent database
├── bot.png                     # AI Assistant avatar
├── logo.png                    # Brand logo
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
└── modules/
    ├── admin.py                # Admin dashboard, analytics & audit logs
    ├── auth.py                 # Authentication, registration & profile onboarding
    ├── chatbot.py              # Gemini AI voice assistant & chat interface
    ├── courses.py              # Free skill training courses catalog
    ├── database.py             # DB schema, persistent settings & SMS logging
    ├── emergency.py            # Emergency contacts, hospitals & NGO finder
    ├── job_matching.py         # AI skill matching algorithm
    ├── language.py             # 12+ Indian language translation dictionaries
    ├── profile.py              # User profile & completion scoring
    ├── resume.py               # 1-click HTML & PDF resume generator
    ├── schemes.py              # Government scheme eligibility checker
    ├── skill_gap.py            # Missing skills analyzer & course recommendations
    ├── states_data.py          # Indian states & districts dataset
    ├── styles.py               # Custom dark theme CSS styling
    └── tracker.py              # Job & Scheme application tracking
```

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/rohan-patil27/community-hub.git
cd community-hub
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
streamlit run app.py
```

### 4. Open in browser
Open **`http://localhost:8501`** in your browser.

---

## 🌐 Deploy to Streamlit Cloud (Live Link)

1. Fork or push this repository to your GitHub account (`https://github.com/rohan-patil27/community-hub`).
2. Visit **[share.streamlit.io](https://share.streamlit.io)** and log in with GitHub.
3. Click **"New App"** and select:
   - **Repository:** `rohan-patil27/community-hub`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy"** to get your public live URL!

---

## 📜 License
This project is open source and available under the [MIT License](LICENSE).
