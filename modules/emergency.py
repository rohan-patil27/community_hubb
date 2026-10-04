import streamlit as st
import pandas as pd
import pydeck as pdk
import urllib.parse
from modules.database import get_conn

TYPE_ICONS = {
    "Mental Health NGO": "🧠", "Crisis Helpline": "📞", "Child Welfare NGO": "👶",
    "Youth & Skill NGO": "🎓", "Government Hospital": "🏥", "Child Helpline": "👦",
    "Women Safety": "👩", "National Emergency": "🚨", "Rehabilitation NGO": "❤️",
    "Homeless NGO": "🏠"
}
CRITICAL_PHONES = {"1098", "181", "112"}

# Precise, distinct coordinates for each contact (no overlapping)
CONTACT_COORDS = {
    "iCall - TISS": (19.0436, 72.9090),
    "Snehi NGO": (19.0843, 72.8360),
    "KEM Hospital": (18.9986, 72.8427),
    "Chhatrapati Shivaji Maharaj Hospital": (19.2025, 72.9915),
    "Sassoon General Hospital": (18.5250, 73.8680),
    "AIIMS Nagpur": (21.0664, 79.0394),
    "District Civil Hospital Nashik": (19.9975, 73.7898),
    "Government Medical College & Hospital (GMC)": (21.0110, 75.5680),
    "Civil Hospital Jalgaon": (21.0040, 75.5600),
    "Red Cross Society Jalgaon": (21.0080, 75.5640),
    "GMCH Sambhajinagar": (19.8900, 75.3200),
    "CPR General Hospital": (16.7050, 74.2433),
    "Dr. VMS Government Civil Hospital": (17.6599, 75.9064),
    "District General Hospital Amravati": (20.9320, 77.7580),
    "Dr. SC Government Medical College": (19.1550, 77.3150),
    "Vasantdada Patil Government Hospital": (16.8524, 74.5815),
    "Kranti-singha Nana Patil District Hospital": (17.6805, 74.0183),
    "Government Medical College & Hospital Latur": (18.4088, 76.5604),
    "Government Medical College & Hospital Akola": (20.7002, 77.0082),
    "District Civil Hospital Ratnagiri": (16.9902, 73.3120),
    "Shri Bhausaheb Hire Government Medical College": (20.9042, 74.7749),
    "Government Medical College Chandrapur": (19.9615, 79.2961),
    "District Civil Hospital Alibag": (18.6414, 72.8722),
    "District General Hospital Palghar": (19.6967, 72.7699),
}

DISTRICT_COORDS = {
    "Mumbai": (19.0760, 72.8777),
    "Thane": (19.2183, 72.9781),
    "Pune": (18.5204, 73.8567),
    "Nagpur": (21.1458, 79.0882),
    "Nashik": (20.0059, 73.7898),
    "Jalgaon": (21.0077, 75.5626),
    "Chhatrapati Sambhajinagar": (19.8762, 75.3433),
    "Kolhapur": (16.7050, 74.2433),
    "Solapur": (17.6599, 75.9064),
    "Amravati": (20.9320, 77.7580),
    "Nanded": (19.1550, 77.3150),
    "Sangli": (16.8524, 74.5815),
    "Satara": (17.6805, 74.0183),
    "Latur": (18.4088, 76.5604),
    "Akola": (20.7002, 77.0082),
    "Ratnagiri": (16.9902, 73.3120),
    "Dhule": (20.9042, 74.7749),
    "Chandrapur": (19.9615, 79.2961),
    "Raigad": (18.6414, 72.8722),
    "Palghar": (19.6967, 72.7699),
}

def show_emergency(t):
    st.markdown("""
    <div class="section-header">
        <div class="section-header-icon">🆘</div>
        <div>
            <h2>Emergency Help & Support</h2>
            <p>Nearby NGOs, hospitals, helplines — available 24/7 with Google Maps Integration</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Critical helplines first
    st.markdown("""
    <div style="background:linear-gradient(135deg,#2d0a0a,#1a0505);border:1px solid #7f1d1d;border-radius:14px;padding:1.5rem;margin-bottom:1.5rem;">
        <div style="font-family:'Sora',sans-serif;font-size:1rem;font-weight:700;color:#f87171;margin-bottom:1rem;">🚨 National Emergency Numbers — Call Free, 24/7</div>
        <div style="display:flex;flex-wrap:wrap;gap:1rem;">
            <div style="background:#3d0505;border:1px solid #991b1b;border-radius:10px;padding:0.8rem 1.2rem;text-align:center;flex:1;min-width:140px;">
                <div style="font-size:2rem;font-weight:800;color:#f87171;">112</div>
                <div style="color:#fca5a5;font-size:0.82rem;">Police • Fire • Ambulance</div>
            </div>
            <div style="background:#3d0505;border:1px solid #991b1b;border-radius:10px;padding:0.8rem 1.2rem;text-align:center;flex:1;min-width:140px;">
                <div style="font-size:2rem;font-weight:800;color:#fbbf24;">1098</div>
                <div style="color:#fde68a;font-size:0.82rem;">Childline — Child Help</div>
            </div>
            <div style="background:#3d0505;border:1px solid #991b1b;border-radius:10px;padding:0.8rem 1.2rem;text-align:center;flex:1;min-width:140px;">
                <div style="font-size:2rem;font-weight:800;color:#a78bfa;">181</div>
                <div style="color:#c4b5fd;font-size:0.82rem;">Women Helpline</div>
            </div>
            <div style="background:#3d0505;border:1px solid #991b1b;border-radius:10px;padding:0.8rem 1.2rem;text-align:center;flex:1;min-width:140px;">
                <div style="font-size:2rem;font-weight:800;color:#34d399;">102</div>
                <div style="color:#6ee7b7;font-size:0.82rem;">Free Ambulance</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        type_filter = st.selectbox("📂 Type", ["All Types", "Government Hospital", "Mental Health NGO",
                                                "Crisis Helpline", "Child Welfare NGO", "Youth & Skill NGO",
                                                "Rehabilitation NGO", "Homeless NGO"], key="em_type")
    with col2:
        districts = [
            "All Districts", "Mumbai", "Thane", "Pune", "Nagpur", "Nashik", "Jalgaon",
            "Chhatrapati Sambhajinagar", "Kolhapur", "Solapur", "Amravati", "Nanded",
            "Sangli", "Satara", "Latur", "Akola", "Ratnagiri", "Dhule", "Chandrapur",
            "Raigad", "Palghar"
        ]
        dist_filter = st.selectbox("📍 District", districts, key="em_dist")

    conn = get_conn()
    c = conn.cursor()
    query = "SELECT * FROM emergency_contacts WHERE type NOT IN ('Child Helpline','Women Safety','National Emergency')"
    params = []
    if type_filter != "All Types":
        query += " AND type=?"
        params.append(type_filter)
    if dist_filter != "All Districts":
        query += " AND (district=? OR district='All')"
        params.append(dist_filter)
    c.execute(query, params)
    contacts = [dict(r) for r in c.fetchall()]
    conn.close()

    # 🗺️ Interactive Color-Coded Map View with Small Crisp Pixel Pins & Hover Tooltips
    map_data = []
    used_coords = set()

    for idx, contact in enumerate(contacts):
        name = contact['name']
        dist = contact['district']
        base_coords = CONTACT_COORDS.get(name) or DISTRICT_COORDS.get(dist)
        
        if base_coords:
            lat, lon = base_coords
            # If coordinates conflict with an existing pin, apply a slight jitter offset
            while (round(lat, 4), round(lon, 4)) in used_coords:
                lat += 0.012
                lon += 0.012
            used_coords.add((round(lat, 4), round(lon, 4)))

            is_hospital = "Hospital" in contact['type']
            # Crisp Red [239, 68, 68] for Hospitals, Bright Blue [59, 130, 246] for NGOs
            color = [239, 68, 68, 255] if is_hospital else [59, 130, 246, 255]
            category = "🏥 Government Hospital" if is_hospital else "🧠 NGO / Helpline"
            
            map_data.append({
                "name": contact['name'],
                "latitude": lat,
                "longitude": lon,
                "type": contact['type'],
                "category": category,
                "district": contact['district'],
                "phone": contact['phone'],
                "address": contact['address'],
                "color": color
            })

    if map_data:
        with st.expander("🗺️ Interactive Color-Coded NGO & Hospital Map", expanded=True):
            st.markdown("""
            <div style='display:flex;flex-wrap:wrap;gap:1.5rem;align-items:center;background:#161b22;padding:0.75rem 1rem;border-radius:10px;border:1px solid #30363d;margin-bottom:0.8rem;font-size:0.85rem;'>
                <div style='display:flex;align-items:center;gap:0.4rem;'><span style='color:#ef4444;font-size:1.2rem;'>🔴</span> <b style='color:#e6edf3;'>Red Dots:</b> Government Hospitals</div>
                <div style='display:flex;align-items:center;gap:0.4rem;'><span style='color:#3b82f6;font-size:1.2rem;'>🔵</span> <b style='color:#e6edf3;'>Blue Dots:</b> NGOs & Helplines</div>
                <div style='color:#94a3b8;margin-left:auto;'>💡 <b>Hover dot</b> to view info card</div>
            </div>
            """, unsafe_allow_html=True)
            
            df_map = pd.DataFrame(map_data)
            avg_lat = df_map['latitude'].mean()
            avg_lon = df_map['longitude'].mean()

            # ScatterplotLayer with pixel-based sizing so pins stay sleek and never bloat or overlap into giant blobs!
            layer = pdk.Layer(
                "ScatterplotLayer",
                df_map,
                get_position=["longitude", "latitude"],
                get_fill_color="color",
                radius_units="pixels",
                get_radius=9,
                radius_min_pixels=6,
                radius_max_pixels=12,
                stroked=True,
                get_line_color=[255, 255, 255, 220],
                get_line_width=2,
                line_width_min_pixels=1.5,
                pickable=True,
                auto_highlight=True
            )

            view_state = pdk.ViewState(
                latitude=avg_lat,
                longitude=avg_lon,
                zoom=6.5 if dist_filter == "All Districts" else 10,
                pitch=0
            )

            r = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip={
                    "html": "<div style='background:#161b22;color:#ffffff;padding:10px 14px;border-radius:10px;border:1px solid #3b82f6;font-family:sans-serif;box-shadow:0 4px 16px rgba(0,0,0,0.5);'>"
                            "<div style='font-size:1rem;font-weight:700;color:#ffffff;'>{name}</div>"
                            "<div style='color:#60a5fa;font-size:0.85rem;margin:0.2rem 0;'>{category} • {type}</div>"
                            "<div style='color:#94a3b8;font-size:0.82rem;'>📍 {address}, {district}</div>"
                            "<div style='color:#34d399;font-size:0.85rem;font-weight:600;margin-top:0.3rem;'>📞 {phone}</div>"
                            "</div>",
                    "style": {"color": "white", "zIndex": "9999"}
                }
            )
            st.pydeck_chart(r)

    st.markdown(f"<div style='color:#8b949e;font-size:0.85rem;margin:1rem 0;'>Showing <b style='color:#60a5fa;'>{len(contacts)}</b> contacts</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    for i, contact in enumerate(contacts):
        icon = TYPE_ICONS.get(contact['type'], "📋")
        is_critical = contact.get('phone','') in CRITICAL_PHONES
        card_class = "emergency-card critical" if is_critical else "emergency-card"
        is_hosp = "Hospital" in contact['type']
        pin_tag = "<span style='color:#ef4444;font-size:0.8rem;font-weight:700;'>🔴 Hospital Pin</span>" if is_hosp else "<span style='color:#3b82f6;font-size:0.8rem;font-weight:700;'>🔵 NGO Pin</span>"

        # Generate Google Maps link
        address_query = urllib.parse.quote(f"{contact['name']}, {contact['address']}, {contact['district']}")
        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={address_query}"

        full_addr = contact['address']
        if contact.get('district') and contact['district'] not in ['All', 'All India'] and contact['district'].lower() not in full_addr.lower():
            full_addr = f"{full_addr}, {contact['district']}"

        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="{card_class}">
                <div style="display:flex;align-items:flex-start;gap:0.75rem;">
                    <span style="font-size:1.8rem;">{icon}</span>
                    <div style="flex:1;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <div style="font-family:'Sora',sans-serif;font-weight:600;color:#e6edf3;font-size:0.95rem;">{contact['name']}</div>
                            {pin_tag}
                        </div>
                        <span class="badge badge-purple" style="font-size:0.72rem;margin:0.3rem 0;">{contact['type']}</span>
                        <div><span class="phone-badge">📞 {contact['phone']}</span></div>
                        <div style="color:#8b949e;font-size:0.8rem;margin-top:0.4rem;">📍 {full_addr}</div>
                        <div style="color:#94a3b8;font-size:0.8rem;margin-top:0.3rem;">🕐 {contact['timing']}</div>
                        <div style="color:#8b949e;font-size:0.8rem;margin-top:0.3rem;padding-top:0.3rem;border-top:1px solid #21262d;">
                            {contact['services']}
                        </div>
                        <div style="margin-top:0.6rem;">
                            <a href="{gmaps_url}" target="_blank" style="text-decoration:none;">
                                <span style="background:linear-gradient(135deg,#1e3a5f,#2563eb);color:#ffffff;border:1px solid #3b82f6;padding:0.35rem 0.75rem;border-radius:8px;font-size:0.78rem;font-weight:600;display:inline-flex;align-items:center;gap:0.3rem;transition:all 0.2s;">
                                    🗺️ Open in Google Maps
                                </span>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Safety tips
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("💡 Safety Tips & Rights", expanded=False):
        st.markdown("""
        <div style="color:#cbd5e1;font-size:0.9rem;line-height:1.8;">
        <b style="color:#60a5fa;font-size:0.95rem;">Your Rights</b><br>
        ✅ You can report a cognizable offence at a police station (Zero FIR provisions apply)<br>
        ✅ Child Helpline 1098 is free and available 24/7<br>
        ✅ Women Helpline 181 is available for women seeking support<br><br>
        <b style="color:#60a5fa;font-size:0.95rem;">In Case of Emergency</b><br>
        🚨 Call 112 for police, fire or ambulance emergency assistance<br>
        📱 Share your location/contact details with trusted people when safe<br>
        🏥 Seek immediate medical attention in a medical emergency<br>
        🆘 If you are unable to speak safely, use available emergency/SOS features or ask a trusted person to call for help
        </div>
        """, unsafe_allow_html=True)
