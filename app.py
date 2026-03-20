import streamlit as st
import google.generativeai as genai
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# إعداد المفتاح
API_KEY = "AIzaSyDAqdEHHSN-dMSq3Ly1LiqVdQxVheSPS8s"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Teaching Boost AI", page_icon="🚀")
st.title("🚀 Teaching Boost - الإصدار الاحترافي")

uploaded_file = st.file_uploader("ارفع ملف الـ PDF هنا", type="pdf")

if uploaded_file:
    with st.spinner("جاري المعالجة... قد تستغرق دقيقة لأول مرة"):
        try:
            # قراءة الملف
            file_bytes = uploaded_file.read()
            
            # محاولة استخدام الموديل المستقر
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            response = model.generate_content([
                "حلل هذا الملف التعليمي بالعربية. المطلوب: 1- درس منظم، 2- ملخص، 3- خمسة أسئلة اختيار من متعدد مع الأجوبة.",
                {'mime_type': 'application/pdf', 'data': file_bytes}
            ])

            if response:
                st.success("✅ تم استخراج البيانات بنجاح!")
                st.markdown(response.text)
                
                # تحويل إلى Word
                doc = Document()
                p = doc.add_paragraph(response.text)
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                
                bio = io.BytesIO()
                doc.save(bio)
                st.download_button("📥 تحميل ملف Word الجاهز", data=bio.getvalue(), file_name="Teaching_Boost.docx")

        except Exception as e:
            st.error(f"عذراً، السيرفر ما زال يتحدث. الخطأ: {e}")
            st.info("إذا استمرت 404، يرجى الضغط على الثلاث نقاط بالأعلى في تطبيق Streamlit واختيار 'Reboot App'.")
