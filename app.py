import streamlit as st
import fitz  # PyMuPDF
import re

# إعدادات واجهة المستخدم
st.set_page_config(page_title="CQC Quiz App", page_icon="🚛", layout="centered")

st.markdown("""
    <style>
    .question-card {
        background-color: #f9f9f9;
        padding: 30px;
        border-radius: 15px;
        border-left: 8px solid #007bff;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        font-size: 22px;
        line-height: 1.6;
        margin-bottom: 20px;
        direction: ltr; /* لأن الأسئلة بالإيطالية */
    }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; }
    </style>
""", unsafe_allow_index=True)

def get_cqc_questions(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    all_text = ""
    for page in doc:
        all_text += page.get_text()
    
    # تنظيف النص واستخراج الأسئلة بناءً على الأرقام (1, 2, 3...)
    # النمط يبحث عن رقم يتبعه نص السؤال
    questions = re.findall(r'\n(\d+)\s*\n(.*?)(?=\n\d+\s*\n|$)', all_text, re.DOTALL)
    return [f"{q[0]}. {q[1].strip()}" for q in questions]

st.title("📖 ملقن أسئلة CQC التفاعلي")
st.write("قم برفع ملف الـ PDF وابدأ التدريب سؤالاً بسؤال.")

uploaded_file = st.file_uploader("اختر ملف cqc pdf.pdf", type="pdf")

if uploaded_file:
    if 'cqc_data' not in st.session_state:
        with st.spinner('جاري معالجة 1736 سؤال...'):
            st.session_state.cqc_data = get_cqc_questions(uploaded_file)
            st.session_state.current_q = 0

    questions = st.session_state.cqc_data
    
    if questions:
        idx = st.session_state.current_q
        total = len(questions)

        # شريط التقدم
        st.progress((idx + 1) / total)
        st.write(f"السؤال {idx + 1} من {total}")

        # عرض السؤال
        st.markdown(f'<div class="question-card">{questions[idx]}</div>', unsafe_allow_index=True)

        # أزرار التحكم
        col1, col2 = st.columns(2)
        with col2:
            if st.button("السؤال التالي ➡️"):
                if idx < total - 1:
                    st.session_state.current_q += 1
                    st.rerun()
        with col1:
            if st.button("⬅️ السؤال السابق"):
                if idx > 0:
                    st.session_state.current_q -= 1
                    st.rerun()
        
        # خيار الذهاب لسؤال محدد
        target_q = st.number_input("اذهب إلى سؤال رقم:", min_value=1, max_value=total, value=idx+1)
        if st.button("انتقال"):
            st.session_state.current_q = target_q - 1
            st.rerun()
    else:
        st.error("تعذر استخراج الأسئلة. تأكد من رفع الملف الصحيح.")
