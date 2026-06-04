import streamlit as st
import pypdf
import asyncio
import edge_tts
import io

# 1. Webpage Configuration
st.set_page_config(
    page_title="AI Storyteller & Narrator", 
    page_icon="🎙️", 
    layout="centered"
)

st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: bold; text-align: center; color: #4A90E2; }
    .sub-title { font-size: 1.1rem; text-align: center; margin-bottom: 2rem; color: #555555; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎙️ AI Emotional Male Voiceover Narrator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Apni PDF upload karein aur payein ek dam real aur cinematic male voiceover narration.</p>', unsafe_allow_html=True)

# 2. File Upload Widget
uploaded_file = st.file_uploader("Apni PDF File Yahan Select Karein", type=["pdf"])

# Edge TTS sound generate karne ke liye async function
async def generate_voiceover(text, voice_name):
    communicate = edge_tts.Communicate(text, voice_name)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

if uploaded_file is not None:
    st.info("📂 PDF file mil gayi hai. Processing shuru ho rahi hai...")
    
    # 3. PDF se Text Extract Karna
    full_text = ""
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    except Exception as e:
        st.error(f"⚠️ PDF padhne me koi dikkat aayi: {e}")
        st.stop()
    
    if not full_text.strip():
        st.error("❌ Is PDF me koi text nahi mila!")
    else:
        with st.expander("📄 Extract kiya hua Text Dekhein (Preview)"):
            st.text_area("PDF Text:", value=full_text, height=150, disabled=True)
            
        # 4. Premium Male Voice Selection
        # en-US-BrianNeural / en-US-RyanNeural aur hi-IN-MadhurNeural sabse best aur real hain
        voice_options = {
            "Hindi Male (Madhur - Deep & Emotional) 🇮🇳": "hi-IN-MadhurNeural",
            "English Male (Liam - Studio Narration) 🇺🇸": "en-US-LiamNeural",
            "English Male (Ryan - Natural Storyteller) 🇺🇸": "en-US-RyanNeural"
        }
        
        selected_voice_label = st.selectbox("🎚️ Apni AI Male Voice Chunyein:", list(voice_options.keys()))
        selected_voice = voice_options[selected_voice_label]

        # 5. Narration Generate Karna
        if st.button("Cinematic Voiceover Taiyar Karein 🚀", use_container_width=True):
            with st.spinner("⏳ High-Quality AI Voiceover banaya ja raha hai... please thoda sa wait karein..."):
                try:
                    # Async function ko Streamlit me chalana
                    audio_bytes = asyncio.run(generate_voiceover(full_text, selected_voice))
                    
                    if audio_bytes:
                        st.success("🎉 Premium Emotional Voiceover bilkul taiyar hai!")
                        
                        # Webpage par audio player dikhana
                        st.audio(audio_bytes, format="audio/mp3")
                        
                        # Download Button
                        st.download_button(
                            label="High-Quality Audio Download Karein 📥",
                            data=audio_bytes,
                            file_name="premium_narration.mp3",
                            mime="audio/mp3",
                            use_container_width=True
                        )
                except Exception as tts_error:
                    st.error(f"❌ Audio banane me error aaya: {tts_error}")
                    st.info("💡 Tip: Internet connection check karein.")
