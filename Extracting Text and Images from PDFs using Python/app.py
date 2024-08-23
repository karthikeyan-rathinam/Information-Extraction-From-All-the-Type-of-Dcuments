import pytesseract
from pdf2image import convert_from_path
import fitz  # PyMuPDF
from PIL import Image
import io
import os
import requests

def download_tesseract_lang_data(lang):
    """Download Tesseract language data if not already present."""
    tessdata_dir = os.path.join(os.getenv('TESSDATA_PREFIX', ''), 'tessdata')
    if not os.path.exists(tessdata_dir):
        os.makedirs(tessdata_dir)

    lang_file = os.path.join(tessdata_dir, f'{lang}.traineddata')
    if not os.path.exists(lang_file):
        url = f'https://github.com/tesseract-ocr/tessdata_best/raw/main/{lang}.traineddata'
        r = requests.get(url)
        with open(lang_file, 'wb') as f:
            f.write(r.content)

def extract_text_and_images(input_pdf_path, output_pdf_path, dpi=300, lang='eng'):
    # Ensure language data is available
    for l in lang.split('+'):
        download_tesseract_lang_data(l)

    # Convert PDF to images
    try:
        images = convert_from_path(input_pdf_path, dpi=dpi)
    except Exception as e:
        print("An error occurred while converting PDF to images:", e)
        print("Ensure Poppler is installed and added to PATH.")
        return None, None

    ocr_text_list = []
    pdf_document = fitz.open()

    for page_num, image in enumerate(images):
        # Perform OCR on the image
        ocr_text = pytesseract.image_to_string(image, lang=lang)
        ocr_text_list.append(ocr_text.strip())

        # Extract text directly from the PDF
        pdf_page = fitz.open(input_pdf_path)[page_num]
        pdf_text = pdf_page.get_text("text")

        # Combine direct text extraction and OCR text
        combined_text = pdf_text + "\n" + ocr_text

        # Convert PIL Image to PyMuPDF Image
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        img_pdf = fitz.open("jpeg", img_byte_arr)

        # Create a new page in the PDF
        pdf_page = pdf_document.new_page(width=img_pdf[0].rect.width, height=img_pdf[0].rect.height)

        # Insert the image into the PDF page
        pdf_page.insert_image(pdf_page.rect, stream=img_byte_arr)

        # Insert the combined text into the PDF page as an invisible layer
        pdf_page.insert_text((0, 0), combined_text, fontsize=0, color=(0, 0, 0), render_mode=2)

    # Save the new PDF document
    pdf_document.save(output_pdf_path)
    pdf_document.close()

    return ocr_text_list

# Usage
input_pdf_path = '/content/yourPDFName.pdf'
output_pdf_path = 'output_path.pdf'
languages = 'eng+spa+fra'  # Example languages: English, Spanish, French
extracted_text = extract_text_and_images(input_pdf_path, output_pdf_path, lang=languages)

# Print or use the extracted OCR text
if extracted_text:
    for page_num, text in enumerate(extracted_text, start=1):
        print(f"Page {page_num} OCR text:")
        print(text)
        print()
