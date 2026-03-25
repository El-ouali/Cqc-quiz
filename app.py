import streamlit as st
import fitz  # PyMuPDF
import re

# إعدادات الصفحة
st.set_page_config(page_title="CQC Quiz", page_icon="🚛", layout="centered")

# إضافة تنسيقات CSS مخصصة لتكبير الخط وترتيب الأزرار
st.markdown("""
    <style>
    /* تكبير خط السؤال */
    .question-text {
        font-size: 28px !important;
        font-weight: bold;
        color: #1E1E1E;
        line-height: 1.6;
        padding: 25px;
        background-color: #f8f9fa;
        border-right: 10px solid #007bff;
        border-radius: 10px;
        margin-bottom: 30px;
        direction: ltr; /* للنص الإيطالي */
        text-align: left;
    }
    
    /* تنسيق الأزرار */
    .stButton>button {
        width: 100%;
        height: 3.5em;
        font-size: 20px !important;
        font-weight: bold;
        border-radius: 15px;
    }
    
    /* زر التالي (أزرق) */
    div[data-testid="column"]:nth-child(2) button {
        background-color: #007bff;
        color: white;
    }

    /* زر السابق (رمادي) */
    div[data-testid="column"]:nth-child(1) button {
        background-color: #eeeeee;
        color: #333;
    }
    </style>
""", unsafe_allow_index=True)

st.title("🚛 مدرب أسئلة CQC")

def extract_cqc(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    
    # البحث عن نمط: رقم يتبعه نص السؤال
    questions = re.findall(r'\n(\d+)\s+(.*?)(?=\n\d+\s+|$)', text, re.DOTALL)
    return [f"{q[0]}. {q[1].strip()}" for q in questions]

uploaded_file = st.file_uploader("قم برفع ملف الـ PDF لبدء الدراسة", type="pdf")

if uploaded_file:
    if 'questions' not in st.session_state:
        with st.spinner('جاري تحضير الأسئلة...'):
            st.session_state.questions = extract_cqc(uploaded_file)
            st.session_state.current_idx = 0

    qs = st.session_state.questions
    
    if qs:
        idx = st.session_state.current_idx
        
        # عرض شريط التقدم بشكل أوضح
        st.write(f"### السؤال {idx + 1} من {len(qs)}")
        st.progress((idx + 1) / len(qs))
        
        # عرض السؤال بخط كبير (باستخدام التنسيق المخصص أعلاه)
        st.markdown(f'<div class="question-text">{qs[idx]}</div>', unsafe_allow_index=True)

        # ترتيب الأزرار: السابق في اليسار (Col 1) والتالي في اليمين (Col 2)
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⬅️ السابق"):
                if idx > 0:
                    st.session_state.current_idx -= 1
                    st.rerun()
        
        with col2:
            if st.button("التالي ➡️"):
                if idx < len(qs) - 1:
                    st.session_state.current_idx += 1
                    st.rerun()

        st.divider()
        
        # القفز السريع لسؤال معين
        jump_col1, jump_col2 = st.columns([2, 1])
        with jump_col1:
            new_idx = st.number_input("انتقل إلى سؤال رقم:", min_value=1, max_value=len(qs), value=idx+1)
        with jump_col2:
            st.write(" ") # مسافة بسيطة
            st.write(" ") 
            if st.button("اذهب"):
                st.session_state.current_idx = int(new_idx) - 1
                st.rerun()
    else:
        st.error("لم نجد أسئلة في الملف، يرجى التأكد من رفع ملف CQC الصحيح.")
else:
    st.info("بانتظار رفع ملف الـ PDF الخاص بك...")
