from typing import Any

class ProcessingResult:
    def __init__(self, success: bool, data: Any, error: str = ""):
        self.success = success
        self.data = data
        self.error = error

    def __str__(self):
        if self.success:
            return f"Success: {self.success}"
        else:
            return f"Failed: {self.error}"

from typing import Union
from PIL import Image
import io

def resize_image_bytes(image_bytes: Union[bytes, bytearray], max_size: int = 1120) -> bytes:
    # Open the image from bytes
    image = Image.open(io.BytesIO(image_bytes))

    # Resize while preserving the aspect ratio
    image.thumbnail((max_size, max_size), Image.LANCZOS)
    # Save the resized image to bytes
    output_bytes = io.BytesIO()
    image.save(output_bytes, format="JPEG")  # Adjust format if needed
    output_bytes.seek(0)

    return output_bytes.getvalue()  # Return the resized image bytes
