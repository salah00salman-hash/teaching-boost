import streamlit as st
import google.generativeai as genai
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
import io

# --- الإعدادات الأساسية ---
API_KEY = "AIzaSyDAqdEHHSN-dMSq3Ly1LiqVdQxVheSPS8s" 

genai.configure(api_key=API_KEY)

# استخدام المسار الكامل للموديل لضمان عدم حدوث خطأ 404
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

st.set_page_config(page_title="Teaching Boost AI", layout="centered", page_icon="🚀")

st.title("🚀 Teaching Boost - المحول الذكي")
st.markdown("### الآن يدعم الملفات المصورة والممسوحة ضوئياً!")

uploaded_file = st.file_uploader("ارفع ملف الـ PDF التعليمي", type="pdf")

if uploaded_file:
    with st.spinner("جاري تحليل صفحات الملف بذكاء Gemini..."):
        try:
            # قراءة بيانات الملف
            pdf_bytes = uploaded_file.read()
            
            # تجهيز الطلب
            prompt = """
            أنت خبير تربوي محترف. قم بقراءة محتوى صفحات هذا الملف بالكامل وحوله إلى:
            1. درس منظم بفقرات واضحة.
            2. ملخص شامل لأهم النقاط في شكل نقاط (Bullet points).
            3. 5 أسئلة اختيار من متعدد مع ذكر الإجابة الصحيحة لكل سؤال.
            ملاحظة: يجب أن يكون الرد باللغة العربية الفصحى وبتنسيق جذاب.
            """
            
            # إرسال البيانات كـ Part مباشر
            response = model.generate_content([
                prompt,
                {'mime_type': 'application/pdf', 'data': pdf_bytes}
            ])
            
            final_result = response.text
            
            st.success("✅ تم استخراج المحتوى وتنظيمه!")
            st.markdown("---")
            st.markdown(final_result)
            
            # إنشاء ملف Word
            doc = Document()
            # إضافة المحتوى
            p = doc.add_paragraph(final_result)
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT # محاذاة لليمين
            
            # حفظ الملف في الذاكرة
            bio = io.BytesIO()
            doc.save(bio)
            
            st.divider()
            st.download_button(
                label="📥 تحميل الدرس بصيغة Word",
                data=bio.getvalue(),
                file_name="Teaching_Boost_Lesson.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
        except Exception as e:
            st.error(f"حدث خطأ تقني: {e}")
