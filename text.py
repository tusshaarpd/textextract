import streamlit as st
from PyPDF2 import PdfReader
import easyocr
from PIL import Image

st.title("Text Extraction App")
st.write("Upload PDFs or images to extract text.")

# File uploader
uploaded_file = st.file_uploader("Upload your file (PDF/Image)")

if uploaded_file:
    try:
        # Handle PDF files
        if uploaded_file.name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            st.write("Extracted Text from PDF:")
            st.text(text)

        # Handle image files
        elif uploaded_file.name.endswith((".png", ".jpg", ".jpeg")):
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Initialize EasyOCR reader
            ocr_reader = easyocr.Reader(['en'])
            extracted_text = ocr_reader.readtext(image, detail=0)

            st.write("Extracted Text from Image:")
            st.text("\n".join(extracted_text))

        else:
            st.error("Unsupported file format. Please upload a PDF or an image.")

    except Exception as e:
        st.error(f"Error: {e}")
