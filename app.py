import streamlit as st
import fitz  # PyMuPDF
import re
from googletrans import Translator # مكتبة الترجمة

# إعداد الصفحة
st.set_page_config(page_title="CQC Quiz & Translate", page_icon="🚛")

# تهيئة المترجم
if 'translator' not in st.session_state:
    st.session_state.translator = Translator()

def extract_cqc(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        # نمط استخراج رقم السؤال والنص
        questions = re.findall(r'\n(\d+)\s+(.*?)(?=\n\d+\s+|$)', text, re.DOTALL)
        return [f"{q[0]}. {q[1].strip()}" for q in questions]
    except:
        return []

st.title("🚛 مدرب CQC (إيطالي - عربي)")

uploaded_file = st.file_uploader("ارفع ملف الـ PDF", type="pdf")

if uploaded_file:
    if 'questions' not in st.session_state:
        st.session_state.questions = extract_cqc(uploaded_file)
        st.session_state.current_idx = 0
        st.session_state.translated_text = "" # مخزن الترجمة

    qs = st.session_state.questions
    
    if qs:
        idx = st.session_state.current_idx
        total = len(qs)
        
        st.write(f"### السؤال {idx + 1} من {total}")
        st.progress((idx + 1) / total)
        
        # عرض السؤال الإيطالي بخط كبير
        st.markdown(f"<div style='text-align: left; direction: ltr; background-color: #f0f2f6; padding: 20px; border-radius: 10px; font-size: 26px; font-weight: bold; border-left: 5px solid #007bff;'>{qs[idx]}</div>", unsafe_allow_html=True)
        
        # زر الترجمة
        if st.button("ترجم إلى العربية 🌍"):
            with st.spinner('جاري الترجمة...'):
                try:
                    translation = st.session_state.translator.translate(qs[idx], src='it', dest='ar')
                    st.session_state.translated_text = translation.text
                except:
                    st.session_state.translated_text = "عذراً، حدث خطأ في الاتصال بخدمة الترجمة."

        # عرض الترجمة إذا كانت موجودة
        if st.session_state.translated_text:
            st.markdown(f"<div style='text-align: right; direction: rtl; background-color: #fff4e5; padding: 20px; border-radius: 10px; font-size: 24px; color: #856404; margin-top: 10px; border-right: 5px solid #ffa500;'>{st.session_state.translated_text}</div>", unsafe_allow_html=True)

        st.write("---")

        # الأزرار
        col_left, col_right = st.columns(2)
        with col_left:
            if st.button("⬅️ السابق"):
                if idx > 0:
                    st.session_state.current_idx -= 1
                    st.session_state.translated_text = "" # تصفير الترجمة للسؤال القادم
                    st.rerun()
        
        with col_right:
            if st.button("التالي ➡️", type="primary"):
                if idx < total - 1:
                    st.session_state.current_idx += 1
                    st.session_state.translated_text = "" # تصفير الترجمة للسؤال القادم
                    st.rerun()

        # قفز سريع
        goto = st.number_input("انتقل للسؤال:", 1, total, idx+1)
        if st.button("اذهب"):
            st.session_state.current_idx = int(goto) - 1
            st.session_state.translated_text = ""
            st.rerun()
