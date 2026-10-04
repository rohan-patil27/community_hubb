import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64
from tempfile import NamedTemporaryFile

from modules.database import get_setting, set_setting

def get_audio_html(text, lang='hi'):
    try:
        tts = gTTS(text=text, lang=lang)
        # Use a temporary file to avoid conflicts
        with NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
        tts.save(temp_path)
        with open(temp_path, "rb") as f:
            audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()
        os.remove(temp_path)
        return f'<audio autoplay controls src="data:audio/mp3;base64,{b64}" style="width:100%; margin-top:10px;"></audio>'
    except Exception as e:
        return f"<div style='color:#f87171;'>Audio Error: {str(e)}</div>"

def show_chatbot(user, t, key_prefix="cb"):
    # Load persistent API key from DB or environment if not in session
    if 'gemini_api_key' not in st.session_state or not st.session_state.gemini_api_key:
        saved_key = os.environ.get('GEMINI_API_KEY') or get_setting('gemini_api_key', '')
        st.session_state.gemini_api_key = saved_key.strip()

    # Compact Header with small Doraemon Avatar
    bot_img_html = ""
    if os.path.exists("bot.png"):
        with open("bot.png", "rb") as f:
            bot_b64 = base64.b64encode(f.read()).decode()
        bot_img_html = f"<img src='data:image/png;base64,{bot_b64}' style='width:50px; height:50px; object-fit:contain; flex-shrink:0;' />"
    
    st.markdown(
        f"""
        <div style='display:flex; align-items:center; gap:10px; background:#0f172a; padding:8px 12px; border-radius:10px; border:1px solid #1e293b; margin-bottom:6px;'>
            {bot_img_html}
            <div>
                <h4 style='margin:0; color:#38bdf8; font-size:1rem; font-weight:700;'>{t('cb_title')}</h4>
                <p style='margin:1px 0 0; color:#94a3b8; font-size:0.75rem;'>{t('cb_desc')}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.gemini_api_key:
        api_key = st.text_input(t('cb_api_prompt'), type="password", key=f"{key_prefix}_api_key_input")
        if st.button(t('cb_save_key'), key=f"{key_prefix}_save_key_btn"):
            if api_key.strip():
                clean_key = api_key.strip()
                st.session_state.gemini_api_key = clean_key
                set_setting('gemini_api_key', clean_key)
                os.environ['GEMINI_API_KEY'] = clean_key
                st.success("API Key saved permanently!")
                st.rerun()
        st.info("Please enter a Gemini API Key to enable the AI Voice Assistant.")
        return

    # Option to change/clear key if already set
    with st.expander("⚙️ API Key Settings / की बदलें", expanded=False):
        c_k1, c_k2 = st.columns([3, 1])
        with c_k1:
            st.caption("API Key permanently saved in local database.")
        with c_k2:
            if st.button("🗑️ Clear Key", key=f"{key_prefix}_clear_key_btn"):
                st.session_state.gemini_api_key = ''
                set_setting('gemini_api_key', '')
                if 'GEMINI_API_KEY' in os.environ:
                    del os.environ['GEMINI_API_KEY']
                st.rerun()
        
    genai.configure(api_key=st.session_state.gemini_api_key)

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Render chat history compactly
    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.markdown(f"<div style='text-align:right; margin:3px 0;'><span style='background:#1e3a5f; padding:6px 12px; border-radius:12px; color:#e6edf3; display:inline-block; max-width:85%; text-align:left; font-size:0.85rem;'>{msg['content']}</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left; margin:3px 0;'><span style='background:#0d2d1a; padding:6px 12px; border-radius:12px; color:#34d399; display:inline-block; max-width:85%; border:1px solid #065f46; font-size:0.85rem;'>{msg['content']}</span></div>", unsafe_allow_html=True)
            if msg.get('audio'):
                st.markdown(msg['audio'], unsafe_allow_html=True)

    # Reply mode toggle
    reply_mode = st.radio(
        "Response Mode / जवाब का प्रकार:", 
        ["🔊 Voice & Text", "📝 Text Only"], 
        horizontal=True,
        key=f"{key_prefix}_reply_mode_radio"
    )

    # Chat input
    user_input = st.chat_input(t('cb_input_placeholder'), key=f"{key_prefix}_chat_input")
    if user_input:
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        
        status_placeholder = st.empty()
        try:
            status_placeholder.info("AI Soch raha hai / Thinking (Gemini API)...")
            current_lang = st.session_state.get('language', 'hindi')
            
            # Fallback model candidates
            candidate_models = [
                "gemini-2.0-flash",
                "gemini-2.0-flash-exp",
                "gemini-1.5-flash-latest",
                "gemini-1.5-pro",
                "gemini-pro"
            ]
            
            # Dynamically fetch models supported by user's API key
            try:
                available = [m.name.replace("models/", "") for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                if available:
                    # Prioritize flash models, then others
                    flash_first = [m for m in available if 'flash' in m] + [m for m in available if 'flash' not in m]
                    for m in reversed(flash_first):
                        if m in candidate_models:
                            candidate_models.remove(m)
                        candidate_models.insert(0, m)
            except Exception:
                pass

            system_prompt = (
                f"You are a helpful, polite, and very simple AI assistant for 'Community Hub', an app for slum residents in India. "
                f"CRITICAL RULE: Always reply in the EXACT SAME language the user speaks to you in. "
                f"If they ask in Hindi (like 'kaise ho'), reply in Hindi. If they ask in English, reply in English. "
                "Keep answers extremely short (1 to 2 short sentences). "
                "If they ask about jobs, schemes, or courses, guide them to check those specific sections in the app."
            )

            response = None
            last_err = None
            for model_name in candidate_models:
                try:
                    model = genai.GenerativeModel(model_name)
                    res = model.generate_content(system_prompt + "\n\nUser: " + user_input)
                    if res and res.text:
                        response = res
                        break
                except Exception as err:
                    last_err = err
                    continue

            if not response or not hasattr(response, 'text') or not response.text:
                raise Exception(f"No working Gemini model found. Error: {last_err}")

            ai_text = response.text
            
            audio_html = None
            if "Voice" in reply_mode:
                status_placeholder.info("Awaaz bana raha hai / Generating Audio (gTTS)...")
                tts_lang = 'mr' if current_lang == 'marathi' else ('en' if current_lang == 'english' else 'hi')
                audio_html = get_audio_html(ai_text, lang=tts_lang)
            
            st.session_state.chat_history.append({
                'role': 'ai', 
                'content': ai_text,
                'audio': audio_html
            })
            status_placeholder.empty()
            st.rerun()
        except Exception as e:
            status_placeholder.error(f"Error: {e}")
