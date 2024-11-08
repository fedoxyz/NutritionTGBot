from typing import Dict, Optional
from utils.json_utils import parse_json_file
#import requests
from logger import logger


def qr_process_receipt(photo_bytes: bytes) -> Optional[Dict]:
    """
    Process the receipt using QR code data. Calls an external API with the QR data.
    """
    return None # To be continued...
    qr_data = extract_qr_code_data(photo_bytes)
    if not qr_data:
        return None

    # Parse the QR data into parameters for the API call
    # Assuming the QR data is a URL-like string with parameters
    try:
        return None
      #  params = dict(param.split('=') for param in qr_data.split('&'))
       # response = requests.get("https://api.example.com/receipt", params=params)
       # response.raise_for_status()  # Raise an error for bad status codes
      #  return parse_json_file(response.json())  # Parse the JSON response
    except Exception as e:
        logger.error(f"Error processing receipt with QR code: {e}")
        return None

def extract_qr_code_data(photo_bytes: bytes) -> Optional[Dict]:
    """
    Extract QR code data from the given image bytes.
    You can use a library like `pyzbar` for QR code scanning.
    """
    from pyzbar.pyzbar import decode
    from PIL import Image
    from io import BytesIO

    try:
        image = Image.open(BytesIO(photo_bytes))
        qr_codes = decode(image)
        if qr_codes:
            # Assuming the first QR code is the one we want
            qr_data = qr_codes[0].data.decode('utf-8')
            return qr_data
    except Exception as e:
        logger.error(f"QR code extraction failed: {e}")
    return None
