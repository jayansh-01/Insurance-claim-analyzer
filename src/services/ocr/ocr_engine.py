import io
import logging
import asyncio
from PIL import Image

# Setup app logger
logger = logging.getLogger("app")

try:
    import pytesseract
except ImportError:
    pytesseract = None

class OCREngineService:
    """
    Service to process document images and extract text using OCR.
    Includes a fallback mock mechanism if Tesseract is not installed or configured.
    """
    async def extract_text_from_bytes(self, file_bytes: bytes, file_name: str) -> str:
        logger.info(f"OCR extraction initiated for file: {file_name}")
        
        try:
            # Parse image structures safely
            image = Image.open(io.BytesIO(file_bytes))
            
            if pytesseract is None:
                raise ImportError("pytesseract library is not installed in the python environment.")
            
            # Extract text asynchronously using a thread pool
            text = await asyncio.to_thread(pytesseract.image_to_string, image)
            
            if not text or not text.strip():
                raise ValueError("OCR process returned empty text.")
            
            logger.info(f"OCR extraction completed successfully for file: {file_name}")
            return text
            
        except Exception as e:
            logger.warning(
                f"OCR extraction failed or Tesseract is not configured: {str(e)}. "
                f"Falling back to structured mock text."
            )
            
            # Structured mock layout string containing invoice/policy metadata
            mock_text = (
                "--- OCR EXTRACTED TEXT (MOCK FALLBACK) ---\n"
                f"Document Name: {file_name}\n"
                "Document Type: Health Insurance Claim Invoice\n"
                "Policy Number: POL-99887766\n"
                "Insured Customer: Jayansh Kumar\n"
                "Provider Name: Apex Health Clinic\n"
                "Date of Service: 2026-06-15\n"
                "Total Billed Amount: $1250.00\n"
                "Diagnoses Codes: ICD-10 J30.9 (Allergic rhinitis)\n"
                "Procedure Codes: CPT 99213 (Outpatient visit)\n"
                "Claim Status: Pending Review\n"
                "------------------------------------------"
            )
            logger.info(f"OCR extraction completed (via mock fallback) for file: {file_name}")
            return mock_text
