Creating a smart invoice parser involves leveraging technologies like Optical Character Recognition (OCR) to extract text from invoice images or PDFs, and using techniques to parse and organize that data. Below is a complete Python program using the Tesseract OCR engine for text extraction and regular expressions for parsing. You'll need to install Tesseract and Python packages like `pytesseract` and `pdf2image`.

```python
import pytesseract
from pdf2image import convert_from_path
import cv2
import re
import os
import sys

# Set the path to your Tesseract-OCR installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    """Extracts text from a given image using OCR."""
    try:
        # Read image using OpenCV
        image = cv2.imread(image_path)
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None


def extract_text_from_pdf(pdf_path):
    """Converts each page of a PDF file to images and extracts text."""
    try:
        images = convert_from_path(pdf_path)
        full_text = ""
        for image in images:
            # Save current page as a temporary file to read it with OpenCV
            temp_image_path = "temp_page.png"
            image.save(temp_image_path, 'PNG')
            # Extract text from the image
            full_text += extract_text_from_image(temp_image_path)
            os.remove(temp_image_path)
        return full_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None


def parse_invoice_data(text):
    """Parses crucial data from the invoice text."""
    try:
        # Regular expressions for common invoice fields
        invoice_data = {
            'invoice_number': re.search(r'Invoice Number:\s*(\w+)', text, re.IGNORECASE),
            'date': re.search(r'Date:\s*([\d/]+)', text, re.IGNORECASE),
            'total_amount': re.search(r'Total\s*Amount:\s*([\d,.]+)', text, re.IGNORECASE),
            'due_date': re.search(r'Due Date:\s*([\d/]+)', text, re.IGNORECASE),
            'customer': re.search(r'Customer:\s*([A-Za-z\s]+)', text, re.IGNORECASE),
        }

        # Extract and organize parsed data
        parsed_data = {}
        for key, match in invoice_data.items():
            if match:
                parsed_data[key] = match.group(1).strip()
            else:
                parsed_data[key] = None  # None for missing fields
        
        return parsed_data
    except Exception as e:
        print(f"Error parsing invoice data: {e}")
        return None


def main(file_path):
    """Main function to extract and parse data from digital invoices."""
    if not os.path.exists(file_path):
        print(f"File path {file_path} does not exist.")
        return

    # Determine file type and extract text
    text = ""
    try:
        if file_path.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        else:  # Assume it's an image
            text = extract_text_from_image(file_path)
        
        if not text:
            print(f"Failed to extract text from {file_path}")
            return
        
        # Parse extracted text
        invoice_data = parse_invoice_data(text)
        if invoice_data:
            print("Parsed Invoice Data:")
            for key, value in invoice_data.items():
                print(f"{key.capitalize()}: {value}")
        else:
            print("No valid invoice data found.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Example usage: python smart_invoice_parser.py invoice.pdf
    if len(sys.argv) != 2:
        print("Usage: python smart_invoice_parser.py <file-path>")
    else:
        main(sys.argv[1])
```

### Notes:
- **Tesseract Installation**: Ensure Tesseract is installed on your system and you update the path in the script for `pytesseract.pytesseract.tesseract_cmd`.
- **Dependency Installation**: Install necessary dependencies using pip:

  ```bash
  pip install pytesseract pdf2image opencv-python
  ```

- **Error Handling**: The script includes basic error handling for file operations, OCR, and parsing operations.
- **Limitations**: The regex patterns assume a standardized invoice format. You may need to adjust them based on specific invoice structures.
- **Enhancements**: Consider using machine learning approaches for more robust data extraction and handling diverse invoice layouts.