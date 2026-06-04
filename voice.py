import streamlit as st
import pypdf
import requests

# Page Configuration
st.set_page_config(page_title="Ultra-Realistic AI Narrator", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: bold; text-align: center; color: #E67E22; }
    .sub-title { font-size: 1.1rem; text-align: center; margin-bottom: 2rem; color: #555555; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎙️ ElevenLabs Ultra-Realistic Narrator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Human-like emotional voiceover jisme real insaan jaisa expression milega.</p>', unsafe_allow_html=True)

# 🔑 APNI API KEY YAHAN PASTE KAREIN
# Note: Is inverted comma "" ke andar apni ElevenLabs se copy ki hui key dalein
ELEVENLABS_API_KEY = "YAHAN_APNI_API_KEY_PASTE_KAREIN"

# File Uploader
uploaded_file = st.file_uploader("Apni PDF File Upload Karein", type=["pdf"])

if uploaded_file is not None:
    full_text = ""
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    except Exception as e:
        st.error(f"⚠️ PDF Error: {e}")
        st.stop()
    
    if not full_text.strip():
        st.error("❌ Is PDF me koi text nahi mila!")
    else:
        with st.expander("📄 Text Preview"):
            st.text_area("PDF Content:", value=full_text, height=120, disabled=True)
            
        # Top premium voices ids
        voice_options = {
            "Adam (Deep, Professional & Narrative - Best for English)": "pNInz6obpgTE5algwJAw",
            "Antoni (Soft, Storyteller & Emotional - Best for Hindi & English)": "ErXwobaYiN019PkySvjV",
            "George (Warm & Engaging Podcaster Voice)": "JBFv7t76vEgYgUCfoJgH"
        }
        selected_voice_label = st.selectbox("🎚️ Premium AI Voice Chunyein:", list(voice_options.keys()))
        voice_id = voice_options[selected_voice_label]

        if st.button("Premium Voiceover Taiyar Karein 🚀", use_container_width=True):
            if ELEVENLABS_API_KEY == "YAHAN_APNI_API_KEY_PASTE_KAREIN" or not ELEVENLABS_API_KEY:
                st.error("⚠️ Please pehle code me apni ElevenLabs API Key daalein!")
                st.stop()
                
            with st.spinner("⏳ ElevenLabs AI Voiceover taiyar kar raha hai..."):
                try:
                    # 🎯 CORRECT URL FOR ELEVENLABS API
                    url = f"https://elevenlabs.io{voice_id}"
                    
                    headers = {
                        "Accept": "audio/mpeg",
                        "Content-Type": "application/json",
                        "xi-api-key": ELEVENLABS_API_KEY
                    }
                    data = {
                        "text": full_text[:3500],  # Free tier safe character limit
                        "model_id": "eleven_multilingual_v2", 
                        "voice_settings": {
                            "stability": 0.45,        
                            "similarity_boost": 0.85, 
                            "style": 0.10,            
                            "use_speaker_boost": True
                        }
                    }
                    
                    response = requests.post(url, json=data, headers=headers)
                    
                    if response.status_code == 200:
                        st.success("🎉 Ultra-Realistic Voiceover Taiyar Hai!")
                        st.audio(response.content, format="audio/mp3")
                        
                        st.download_button(
                            label="Premium Audio Download Karein 📥",
                            data=response.content,
                            file_name="elevenlabs_narration.mp3",
                            mime="audio/mp3",
                            use_container_width=True
                        )
                    else:
                        st.error(f"❌ ElevenLabs Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
