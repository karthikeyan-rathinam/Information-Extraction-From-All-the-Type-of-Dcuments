![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)![Kaggle](https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white)![Google Drive](https://img.shields.io/badge/Google%20Drive-4285F4?style=for-the-badge&logo=googledrive&logoColor=white)![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)![Kali](https://img.shields.io/badge/Kali-268BEE?style=for-the-badge&logo=kalilinux&logoColor=white)![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)![Google](https://img.shields.io/badge/google-4285F4?style=for-the-badge&logo=google&logoColor=white)![DuckDuckGo](https://img.shields.io/badge/DuckDuckGo-DE5833?style=for-the-badge&logo=DuckDuckGo&logoColor=white)![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

[![GitHub](https://img.shields.io/badge/GitHub-181717.svg?style=for-the-badge&logo=GitHub&logoColor=white)](https://github.com/karthikeyan-rathinam/)
[![Linkedin](https://img.shields.io/badge/LinkedIn-0A66C2.svg?style=for-the-badge&logo=LinkedIn&logoColor=white)](https://www.linkedin.com/in/karthikeyanrathinam/)
[![YouTube](https://img.shields.io/badge/YouTube-FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)](https://www.youtube.com/@linkagethink)
[![Gmail](https://img.shields.io/badge/Gmail-EA4335.svg?style=for-the-badge&logo=Gmail&logoColor=white)](mailto:karthikeyanr1801@gmail.com)

### **Extracting Text and Images from PDFs using Python: A Step-by-Step Guide**

In the digital age, the ability to extract text and images from PDF files is crucial for tasks such as document processing, data analysis, and more. This blog post will guide you through a Python script designed to extract text and images from a PDF file using several powerful libraries, including `pytesseract`, `pdf2image`, `PyMuPDF`, and `PIL`. We will also explore how to handle multi-language support for Optical Character Recognition (OCR) using Tesseract. Let's dive into the code and understand how it works.

---

### **Installation of Required Libraries and Dependencies**

To get started, you need to install the necessary libraries and system packages. Here’s how you can set up your environment:

```bash
!pip install pytesseract pdf2image Pillow pymupdf requests
!sudo apt-get update
!sudo apt-get install poppler-utils tesseract-ocr
```

- **`pytesseract`**: Python wrapper for Google's Tesseract-OCR Engine. Used for OCR on images.
- **`pdf2image`**: Converts PDF files into a sequence of images.
- **`Pillow`**: Python Imaging Library for opening, manipulating, and saving image files.
- **`pymupdf` (fitz)**: A Python binding for the MuPDF PDF and XPS viewer, used for extracting text and handling PDFs.
- **`requests`**: Simple HTTP library for Python, used here to download language data files.

System-level packages like `poppler-utils` (required by `pdf2image` for converting PDFs to images) and `tesseract-ocr` (the Tesseract OCR engine itself) also need to be installed.

### **Importing Required Libraries**

```python
import pytesseract
from pdf2image import convert_from_path
import fitz  # PyMuPDF
from PIL import Image
import io
import os
import requests
```

- Import the libraries you installed. Each of these will be used in different parts of the script to handle PDF conversion, text extraction, and image processing.

### **Function to Download Tesseract Language Data**

```python
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
```

- This function ensures that the required Tesseract language data files are available for OCR. If a language's trained data file is not found locally, it is downloaded from GitHub.
- `tessdata_dir`: Directory where Tesseract language data is stored.
- `lang_file`: Path to the specific language's trained data file.

### **Function to Extract Text and Images from a PDF**

```python
def extract_text_and_images(input_pdf_path, output_pdf_path, dpi=300, lang='eng'):
    # Ensure language data is available
    for l in lang.split('+'):
        download_tesseract_lang_data(l)
```

- **`extract_text_and_images`**: This is the main function that takes the input PDF file, converts it to images, performs OCR to extract text, and saves the output as a new PDF.
- **`input_pdf_path`**: Path to the input PDF file.
- **`output_pdf_path`**: Path to save the output PDF file.
- **`dpi`**: Resolution of images generated from PDF pages (default is 300).
- **`lang`**: Language(s) for OCR. Multiple languages can be specified, separated by a plus sign (`+`).

#### **Convert PDF to Images**

```python
    # Convert PDF to images
    try:
        images = convert_from_path(input_pdf_path, dpi=dpi)
    except Exception as e:
        print("An error occurred while converting PDF to images:", e)
        print("Ensure Poppler is installed and added to PATH.")
        return None, None
```

- **`convert_from_path`**: This function from the `pdf2image` library converts each page of the PDF into an image. The resolution is set by the `dpi` parameter.
- Error handling ensures that if the conversion fails (possibly due to missing Poppler), a message is displayed.

#### **Initialize Lists and PDF Document**

```python
    ocr_text_list = []
    pdf_document = fitz.open()
```

- **`ocr_text_list`**: A list to store the OCR text for each page.
- **`pdf_document`**: A new PDF document is created using `fitz.open()` from the `PyMuPDF` library.

#### **Loop Through Each Page Image and Extract Text**

```python
    for page_num, image in enumerate(images):
        # Perform OCR on the image
        ocr_text = pytesseract.image_to_string(image, lang=lang)
        ocr_text_list.append(ocr_text.strip())

        # Extract text directly from the PDF
        pdf_page = fitz.open(input_pdf_path)[page_num]
        pdf_text = pdf_page.get_text("text")

        # Combine direct text extraction and OCR text
        combined_text = pdf_text + "\n" + ocr_text
```

- **OCR Process**: Uses `pytesseract.image_to_string()` to perform OCR on each image and extract text.
- **Direct Text Extraction**: Extracts text directly from the PDF using PyMuPDF's `get_text()` method.
- **Combining Text**: Both OCR text and direct text are combined to ensure accuracy and completeness.

#### **Convert Image to PyMuPDF Format and Insert into PDF**

```python
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
```

- **Image Conversion**: Converts the PIL Image object to a byte array and then opens it as a PyMuPDF image object.
- **Create New Page**: Adds a new page to the output PDF.
- **Insert Image and Text**: The image is inserted into the page, and the combined text is inserted as an invisible layer (using `fontsize=0`).

#### **Save the PDF Document**

```python
    # Save the new PDF document
    pdf_document.save(output_pdf_path)
    pdf_document.close()

    return ocr_text_list
```

- **Save and Close**: The newly created PDF with images and extracted text is saved to the specified output path.
- **Return**: The function returns a list of OCR texts for further processing or display.

### **Using the Script**

```python
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
```

- **Paths**: Specify the path to your input PDF and where you want to save the output PDF.
- **Languages**: Example demonstrates using multiple languages (English, Spanish, French).
- **Print Extracted Text**: If text is extracted, it is printed out page-by-page.

---

### **Conclusion and Exercises**

This script demonstrates how to use Python libraries to extract text and images from PDFs, leveraging OCR with Tesseract for improved accuracy. By combining direct text extraction and OCR, we can handle a wide range of document types, including those with scanned images or embedded text.

**Exercises:**

1. **Modify Language Support**: Add support for more languages or customize the language detection.
2. **Error Handling**: Improve the error handling in the script to make it more robust against different types of PDF structures or content.
3. **Output Formats**: Adapt the script to save the extracted text in different formats (e.g., TXT, DOCX).
4. **Batch Processing**: Expand the script to handle multiple PDFs in a directory.

By understanding the detailed workings of this script, you can adapt and extend it for various document processing tasks, from simple text extraction to complex multi-language document analysis. Happy coding!

## **Contributing**
Contributions to this project are welcome! If you'd like to contribute, please open an issue or submit a pull request.

## **License**
This project is licensed under the MIT License.

## **Follow**

[![GitHub](https://img.shields.io/badge/GitHub-181717.svg?style=for-the-badge&logo=GitHub&logoColor=white)](https://github.com/karthikeyan-rathinam/)
[![Linkedin](https://img.shields.io/badge/LinkedIn-0A66C2.svg?style=for-the-badge&logo=LinkedIn&logoColor=white)](https://www.linkedin.com/in/karthikeyanrathinam/)
[![YouTube](https://img.shields.io/badge/YouTube-FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)](https://www.youtube.com/@linkagethink)
[![Gmail](https://img.shields.io/badge/Gmail-EA4335.svg?style=for-the-badge&logo=Gmail&logoColor=white)](mailto:karthikeyanr1801@gmail.com)
