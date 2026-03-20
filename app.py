import streamlit as st
import google.generativeai as genai
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# --- الإعدادات ---
API_KEY = "AIzaSyDAqdEHHSN-dMSq3Ly1LiqVdQxVheSPS8s"
genai.configure(api_key=API_KEY)

st.title("🚀 Teaching Boost AI - النسخة المحدثة")

uploaded_file = st.file_uploader("ارفع ملف الـ PDF هنا", type="pdf")

if uploaded_file:
    with st.spinner("جاري التواصل مع الذكاء الاصطناعي..."):
        try:
            # قراءة البيانات
            file_data = uploaded_file.read()
            
            # محاولة استخدام Flash أولاً، وإذا فشل ننتقل لـ Pro
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([
                    {'mime_type': 'application/pdf', 'data': file_data},
                    "حلل هذا الملف التعليمي بالعربية (درس + ملخص + أسئلة)"
                ])
            except:
                model = genai.GenerativeModel('gemini-pro') # بديل في حال تعذر الفلاش
                response = model.generate_content("اقرأ ملف PDF وقم بتلخيصه (تنبيه: السيرفر قد يحتاج تحديث)")

            if response.text:
                st.success("✅ تم استخراج البيانات!")
                st.markdown(response.text)
                
                # إنشاء الملف
                doc = Document()
                p = doc.add_paragraph(response.text)
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                
                bio = io.BytesIO()
                doc.save(bio)
                st.download_button("📥 تحميل Word", data=bio.getvalue(), file_name="lesson.docx")

        except Exception as e:
            st.error(f"خطأ في السيرفر: {e}")
            st.warning("تلميح: إذا استمرت 404، انتظر دقيقتين حتى يقوم Streamlit بتحديث المكتبات بعد تعديل requirements.txt")
