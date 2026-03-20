import streamlit as st
import google.generativeai as genai
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# --- الإعدادات الأساسية ---
API_KEY = "AIzaSyDAqdEHHSN-dMSq3Ly1LiqVdQxVheSPS8s" 

# إعداد الـ API
genai.configure(api_key=API_KEY)

# استخدام اسم الموديل بدون أي بادئات v1beta لضمان الاستقرار
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Teaching Boost AI", layout="centered")

st.title("🚀 Teaching Boost - النسخة المستقرة")

uploaded_file = st.file_uploader("ارفع ملف الـ PDF هنا", type="pdf")

if uploaded_file:
    with st.spinner("جاري المعالجة..."):
        try:
            # قراءة الملف كبيانات
            file_data = uploaded_file.read()
            
            # الطلب
            prompt = "أنت خبير تعليمي، اقرأ هذا الملف وحوله لدرس منظم وملخص و5 أسئلة بالعربية."
            
            # الإرسال بأبسط صورة ممكنة
            response = model.generate_content([
                {'mime_type': 'application/pdf', 'data': file_data},
                prompt
            ])
            
            if response.text:
                st.success("✅ تم بنجاح!")
                st.markdown(response.text)
                
                # إنشاء ملف Word بسيط
                doc = Document()
                p = doc.add_paragraph(response.text)
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                
                bio = io.BytesIO()
                doc.save(bio)
                
                st.download_button("📥 تحميل ملف Word", data=bio.getvalue(), file_name="lesson.docx")
            
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
            st.info("نصيحة: إذا استمر الخطأ، جرب تحديث مفتاح الـ API من Google AI Studio.")
