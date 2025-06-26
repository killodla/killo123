import streamlit as st
import easyocr
import requests
import re
from PIL import Image
import io

# ---------------------------
# 이메일 유효성 검사 함수
# ---------------------------
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# ---------------------------
# 번역 함수 (MyMemory API 사용)
# ---------------------------
def translate_text(text, source_lang='auto', target_lang='en'):
    url = "https://api.mymemory.translated.net/get"
    params = {
        'q': text,
        'langpair': f'{source_lang}|{target_lang}'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['responseData']['translatedText']
    else:
        return "❌ 번역 실패"

# ---------------------------
# EasyOCR 리더 생성 (영어, 한국어)
# ---------------------------
reader = easyocr.Reader(['en', 'ko'], gpu=False)

# ---------------------------
# Streamlit UI 구성
# ---------------------------
st.set_page_config(page_title="OCR 번역기", layout="centered")
st.title("📸 이미지 텍스트 추출 및 번역기")

# 이메일 입력 받기
st.subheader("1️⃣ 이메일 입력")
email = st.text_input("이메일을 입력하세요 (예: example@email.com)")

# 이미지 업로드 받기
st.subheader("2️⃣ 이미지 업로드")
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

# 언어 선택
st.subheader("3️⃣ 번역할 언어 선택")
target_lang = st.selectbox("번역 언어", ['en', 'ko', 'ja', 'zh', 'fr', 'de', 'es'])

# 실행 버튼
if st.button("🚀 텍스트 인식 및 번역 실행"):

    # 이메일 검사
    if not email:
        st.error("❗ 이메일을 입력해주세요.")
    elif not is_valid_email(email):
        st.error("❗ 유효하지 않은 이메일 형식입니다.")
    elif not uploaded_file:
        st.error("❗ 이미지를 업로드해주세요.")
    else:
        # 이미지 표시
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", use_column_width=True)

        # OCR 수행
        with st.spinner("🔍 이미지에서 텍스트 인식 중..."):
            image_bytes = uploaded_file.read()
            results = reader.readtext(image_bytes)

        # 결과 처리
        if results:
            st.subheader("📝 인식된 텍스트:")
            full_text = ""
            for bbox, text, conf in results:
                st.write(f"- {text}")
                full_text += text + " "

            # 번역 수행
            with st.spinner("🌐 번역 중..."):
                translated = translate_text(full_text, target_lang=target_lang)
                st.subheader("📘 번역 결과:")
                st.success(translated)
        else:
            st.warning("⚠️ 텍스트를 인식하지 못했습니다.")
