import streamlit as st
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader
from transformers import pipeline
import os

# Title and Description
st.title("Text Extraction App")
st.caption("Upload PDFs or Images to extract text. Optionally, summarize the extracted text using Hugging Face models.")

# Function to extract text from an image
def extract_text_from_image(image):
    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"Error extracting text from image: {e}")
        return ""

# Function to extract text from a PDF
def extract_text_from_pdf(pdf):
    try:
        reader = PdfReader(pdf)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

# Hugging Face Summarization Pipeline
@st.cache_resource
def load_summarizer():
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        return summarizer
    except Exception as e:
        st.error(f"Error loading summarization model: {e}")
        return None

summarizer = load_summarizer()

# File Upload
uploaded_file = st.file_uploader("Upload a PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Extract text based on file type
    if uploaded_file.type == "application/pdf":
        with st.spinner("Extracting text from PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)
    else:
        with st.spinner("Extracting text from Image..."):
            image = Image.open(uploaded_file)
            extracted_text = extract_text_from_image(image)

    # Display extracted text
    if extracted_text:
        st.subheader("Extracted Text:")
        st.text_area("", extracted_text, height=300)

        # Option to summarize the text
        if summarizer:
            if st.button("Summarize Text"):
                with st.spinner("Summarizing text..."):
                    try:
                        summary = summarizer(extracted_text, max_length=130, min_length=30, do_sample=False)
                        st.subheader("Summarized Text:")
                        st.write(summary[0]['summary_text'])
                    except Exception as e:
                        st.error(f"Error during summarization: {e}")
    else:
        st.warning("No text extracted. Please check the uploaded file.")

# Add a footer
st.write("Powered by [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and [Hugging Face Transformers](https://huggingface.co/)")
