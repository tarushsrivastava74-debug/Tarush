import streamlit as st
import pypdf
from kokoro import KPipeline
import soundfile as sf
import numpy as np
import io

# Page Configuration
st.set_page_config(page_title="Ultra-Realistic Free AI Narrator", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: bold; text-align: center; color: #9B59B6; }
    .sub-title { font-size: 1.1rem; text-align: center; margin-bottom: 2rem; color: #555555; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎙️ Kokoro Ultra-Realistic Free Narrator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Bina kisi limit aur bina kisi API Key ke premium human-like voiceover generator.</p>', unsafe_allow_html=True)

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
            
        # Best available real voices in Kokoro (American & British English)
        # Note: Kokoro is best optimized for English content right now.
        voice_options = {
            "Adam (Deep & Executive Male Voice)": "am_adam",
            "Michael (Professional Storyteller Male)": "am_michael",
            "George (Warm British Podcaster Male)": "bm_george",
            "Bella (Soft & Clear Female Voice)": "af_bella"
        }
        selected_voice_label = st.selectbox("🎚️ Premium Free Voice Chunyein:", list(voice_options.keys()))
        voice_id = voice_options[selected_voice_label]

        if st.button("Cinematic Voiceover Taiyar Karein 🚀", use_container_width=True):
            with st.spinner("⏳ Kokoro AI high-quality audio pack load kar raha hai... isme pehli baar thoda waqt lag sakta hai..."):
                try:
                    # Initialize the pipeline (language code 'a' for American English)
                    # For British voices like George, it adapts internally
                    pipeline = KPipeline(lang_code='a')
                    
                    # Generate audio chunks using generator
                    generator = pipeline(full_text, voice=voice_id, speed=1, split_pattern=r'\n|(?<=[.!?])\s+')
                    
                    audio_chunks = []
                    for gs, ps, audio in generator:
                        if audio is not None:
                            audio_chunks.append(audio)
                    
                    if audio_chunks:
                        # Combine all audio pieces smoothly
                        full_audio = np.concatenate(audio_chunks)
                        
                        # Convert numpy array to temporary mp3 byte array for player
                        buffer = io.BytesIO()
                        sf.write(buffer, full_audio, 24000, format='WAV', subtype='PCM_16')
                        buffer.seek(0)
                        
                        st.success("🎉 Studio-Quality Free Voiceover Taiyar Hai!")
                        st.audio(buffer, format="audio/wav")
                        
                        st.download_button(
                            label="High-Quality Audio Download Karein 📥",
                            data=buffer,
                            file_name="kokoro_narration.wav",
                            mime="audio/wav",
                            use_container_width=True
                        )
                    else:
                        st.error("❌ Audio generate nahi ho paya.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    st.info("💡 Tip: Kokoro model files download karne me thoda waqt leta hai, internet check karein.")
