import streamlit as st
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="CQC Quiz", page_icon="🚛")

# عنوان البرنامج
st.title("🚛 ملقن أسئلة CQC")

def extract_cqc(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    
    # تقسيم الأسئلة بناءً على الأرقام في بداية السطر
    # ملفك يبدأ بـ 1 ثم السؤال، ثم 2 ثم السؤال...
    questions = re.findall(r'\n(\d+)\s+(.*?)(?=\n\d+\s+|$)', text, re.DOTALL)
    return [f"Suaestione {q[0]}: {q[1].strip()}" for q in questions]

uploaded_file = st.file_uploader("ارفع ملف الـ PDF هنا", type="pdf")

if uploaded_file:
    if 'questions' not in st.session_state:
        st.session_state.questions = extract_cqc(uploaded_file)
        st.session_state.current_idx = 0

    qs = st.session_state.questions
    
    if qs:
        idx = st.session_state.current_idx
        
        # عرض التقدم والسؤال
        st.write(f"**التقدم:** {idx + 1} / {len(qs)}")
        
        # صندوق السؤال بتنسيق بسيط
        st.info(qs[idx])

        # أزرار التحكم
        col1, col2 = st.columns(2)
        with col2:
            if st.button("السؤال التالي ➡️"):
                if idx < len(qs) - 1:
                    st.session_state.current_idx += 1
                    st.rerun()
        with col1:
            if st.button("⬅️ السابق"):
                if idx > 0:
                    st.session_state.current_idx -= 1
                    st.rerun()
        
        # رقم السؤال للقفز السريع
        new_idx = st.number_input("انتقل إلى سؤال رقم:", min_value=1, max_value=len(qs), value=idx+1)
        if st.button("Go"):
            st.session_state.current_idx = int(new_idx) - 1
            st.rerun()
    else:
        st.error("لم أتمكن من قراءة الأسئلة، تأكد من رفع ملف cqc pdf.pdf")
