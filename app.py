import streamlit as st
import pypdf
from gtts import gTTS
import io

# Page Configuration
st.set_page_config(page_title="Fast AI Voiceover Narrator", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: bold; text-align: center; color: #1ABC9C; }
    .sub-title { font-size: 1.1rem; text-align: center; margin-bottom: 2rem; color: #555555; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎙️ Upgraded Anti-Lag AI Voiceover</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Badi se badi PDF ke liye lag-free, free aur unlimited audio generator.</p>', unsafe_allow_html=True)

# Function to split text into safe paragraphs (Crash se bachne ke liye)
def get_text_chunks(text, max_chars=2000):
    paragraphs = text.split("\n")
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) < max_chars:
            current_chunk += para + "\n"
        else:
            if current_chunk: chunks.append(current_chunk)
            current_chunk = para + "\n"
    if current_chunk: chunks.append(current_chunk)
    return chunks

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
            
        lang_options = {"English (Clear US Accent)": "en", "Hindi (हिंदी साफ़ आवाज़)": "hi"}
        selected_lang = st.selectbox("🎙️ Voiceover ki Bhasha Chunyein:", list(lang_options.keys()))
        lang_code = lang_options[selected_lang]

        if st.button("Voiceover Taiyar Karein 🚀", use_container_width=True):
            # Text ko safe chunks mein todna
            text_chunks = get_text_chunks(full_text)
            
            progress_bar = st.progress(0.0)
            status_text = st.empty()
            status_text.text("⏳ Audio chunks generate ho rahe hain... Please wait...")
            
            try:
                final_audio = io.BytesIO()
                total_chunks = len(text_chunks)
                
                # Ek-ek chunk ka audio banakar smoothly jodna
                for idx, chunk in enumerate(text_chunks):
                    if not chunk.strip(): continue
                    
                    tts = gTTS(text=chunk, lang=lang_code, slow=False)
                    chunk_fp = io.BytesIO()
                    tts.write_to_fp(chunk_fp)
                    
                    final_audio.write(chunk_fp.getvalue())
                    progress_bar.progress((idx + 1) / total_chunks)
                
                final_audio.seek(0)
                status_text.empty()
                
                st.success("🎉 Voiceover kamyabi se taiyar ho gaya hai!")
                st.audio(final_audio, format="audio/mp3")
                
                st.download_button(
                    label="Audio Download Karein 📥",
                    data=final_audio,
                    file_name="unlimited_narration.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )
            except Exception as e:
                status_text.empty()
                st.error(f"❌ Error: {e}")
