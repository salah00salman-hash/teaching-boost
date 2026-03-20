import streamlit as st
import google.generativeai as genai
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
import io

# --- الإعدادات الأساسية ---
API_KEY = "AIzaSyDAqdEHHSN-dMSq3Ly1LiqVdQxVheSPS8s" 

genai.configure(api_key=API_KEY)
# نستخدم موديل يدعم الرؤية (Vision)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Teaching Boost AI", layout="centered", page_icon="🚀")

st.title("🚀 Teaching Boost - المحول الذكي")
st.markdown("### الآن يدعم الملفات المصورة والممسوحة ضوئياً!")

uploaded_file = st.file_uploader("ارفع ملف الـ PDF التعليمي", type="pdf")

if uploaded_file:
    with st.spinner("جاري تحليل صفحات الملف بذكاء Gemini..."):
        try:
            # تحويل ملف الـ PDF إلى بيانات يفهمها Gemini مباشرة
            pdf_data = uploaded_file.read()
            
            prompt = """
            أنت خبير تربوي. قم بقراءة محتوى صفحات هذا الملف (حتى لو كانت صوراً) وحوله إلى:
            1. درس منظم بفقرات واضحة.
            2. ملخص شامل لأهم النقاط.
            3. 5 أسئلة اختيار من متعدد مع الإجابات الصحيحة.
            ملاحظة: استخرج النص بدقة باللغة العربية.
            """
            
            # إرسال الملف كـ "بيانات" مباشرة للموديل
            response = model.generate_content([prompt, {'mime_type': 'application/pdf', 'data': pdf_data}])
            final_result = response.text
            
            st.success("✅ تمت المعالجة بنجاح!")
            st.write(final_result)
            
            # إنشاء ملف Word
            doc = Document()
            p = doc.add_paragraph(final_result)
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            
            bio = io.BytesIO()
            doc.save(bio)
            
            st.download_button("📥 تحميل الدرس بصيغة Word", data=bio.getvalue(), file_name="Lesson.docx")
            
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
