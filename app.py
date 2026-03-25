import streamlit as st
import fitz  # PyMuPDF
import re

# إعداد الصفحة بدون تنسيقات معقدة في البداية لتجنب الخطأ
st.set_page_config(page_title="CQC Quiz", page_icon="🚛")

# وظيفة استخراج الأسئلة
def extract_cqc(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        # نمط البحث عن رقم يتبعه نص
        questions = re.findall(r'\n(\d+)\s+(.*?)(?=\n\d+\s+|$)', text, re.DOTALL)
        return [f"{q[0]}. {q[1].strip()}" for q in questions]
    except Exception as e:
        return []

st.title("🚛 مدرب أسئلة CQC")

uploaded_file = st.file_uploader("ارفع ملف الـ PDF الخاص بك", type="pdf")

if uploaded_file:
    if 'questions' not in st.session_state:
        st.session_state.questions = extract_cqc(uploaded_file)
        st.session_state.current_idx = 0

    qs = st.session_state.questions
    
    if qs:
        idx = st.session_state.current_idx
        total = len(qs)
        
        # معلومات التقدم
        st.subheader(f"السؤال {idx + 1} من {total}")
        st.progress((idx + 1) / total)
        
        # عرض السؤال بخط كبير جداً باستخدام HTML بسيط (سطر واحد لتجنب الخطأ)
        st.markdown(f"<h1 style='text-align: left; direction: ltr; background-color: #f0f2f6; padding: 20px; border-radius: 10px; font-size: 30px;'>{qs[idx]}</h1>", unsafe_allow_html=True)
        
        st.write("---") # خط فاصل

        # ترتيب الأزرار: السابق يسار، التالي يمين
        col_left, col_right = st.columns(2)
        
        with col_left:
            if st.button("⬅️ السابق (Indietro)"):
                if idx > 0:
                    st.session_state.current_idx -= 1
                    st.rerun()
        
        with col_right:
            # استخدام type='primary' لجعل زر التالي ملوناً وأوضح
            if st.button("التالي (Avanti) ➡️", type="primary"):
                if idx < total - 1:
                    st.session_state.current_idx += 1
                    st.rerun()

        # ميزة الانتقال السريع
        st.write("")
        goto_idx = st.number_input("انتقل إلى سؤال رقم:", min_value=1, max_value=total, value=idx+1)
        if st.button("انتقل الآن"):
            st.session_state.current_idx = int(goto_idx) - 1
            st.rerun()
            
    else:
        st.error("فشل استخراج الأسئلة. تأكد من رفع ملف PDF يحتوي على نص.")
else:
    st.info("الرجاء اختيار ملف الـ PDF من هاتفك.")
