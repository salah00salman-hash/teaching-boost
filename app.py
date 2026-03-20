import streamlit as st
import google.generativeai as genai
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
import pdfplumber
import io

# --- الإعدادات الأساسية ---
# تم وضع مفتاح الـ API الخاص بك هنا
API_KEY = "AIzaSyDAqdEHHSN-dMSq3Ly1LiqVdQxVheSPS8s" 

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Teaching Boost AI", layout="centered", page_icon="🚀")

# --- واجهة المستخدم ---
st.title("🚀 Teaching Boost - المحول الذكي")
st.markdown("""
### أهلاً بك في أداة تحويل المحتوى التعليمي
هذه الأداة تقوم باستخراج النص من الـ PDF، تنظيمه، تلخيصه، وإنشاء أسئلة عليه باستخدام ذكاء **Gemini**.
""")

uploaded_file = st.file_uploader("ارفع ملف الـ PDF التعليمي (باللغة العربية)", type="pdf")

if uploaded_file:
    with st.spinner("جاري قراءة الـ PDF ومعالجته بذكاء Gemini..."):
        # 1. استخراج النص من الـ PDF
        text_content = ""
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text_content += extracted + "\n"
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

        if text_content:
            # 2. إرسال النص لـ Gemini للتحليل والتحويل لدرس
            prompt = f"""
            أنت خبير تربوي ومصمم محتوى تعليمي محترف. 
            قم بتحويل النص العربي التالي إلى "درس تعليمي متكامل" يتكون من:
            1. عنوان جذاب ومقدمة بسيطة.
            2. شرح منظم للمحتوى في فقرات واضحة.
            3. ملخص شامل لأهم النقاط (Bullet points).
            4. بنك أسئلة يحتوي على 5 أسئلة اختيار من متعدد مع ذكر الإجابة الصحيحة لكل سؤال.
            
            ملاحظة: حافظ على لغة عربية سليمة وتنسيق احترافي.
            
            النص المستخرج:
            {text_content}
            """
            
            try:
                response = model.generate_content(prompt)
                final_result = response.text
                
                st.success("✅ تمت معالجة الدرس بنجاح!")
                st.divider()
                st.markdown("### 📝 معاينة الدرس المنظم:")
                st.write(final_result)
                
                # 3. إنشاء ملف Word وتنسيقه للعربية (RTL)
                doc = Document()
                
                # إعدادات الخط الافتراضي
                style = doc.styles['Normal']
                font = style.font
                font.name = 'Arial'
                font.size = Pt(13)
                
                # إضافة النص مع المحاذاة لليمين
                paragraph = doc.add_paragraph(final_result)
                paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                
                # حفظ الملف في ذاكرة مؤقتة (Buffer) للتحميل
                bio = io.BytesIO()
                doc.save(bio)
                
                st.divider()
                st.download_button(
                    label="📥 تحميل الدرس كاملاً بصيغة Word",
                    data=bio.getvalue(),
                    file_name="Teaching_Boost_Lesson.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                st.error(f"حدث خطأ في الاتصال بالذكاء الاصطناعي: {e}")
        else:
            st.warning("لم نتمكن من استخراج نص واضح من هذا الملف، تأكد أنه ليس ملف صور فقط.")

st.info("ملاحظة: هذا التطبيق مدعوم بذكاء Gemini 1.5 Flash")