# main.py
from typing import Callable, TypeVar
from pipelines import create_vision_pipeline, create_classification_pipeline
from functools import lru_cache

T = TypeVar('T')  # Input type
R = TypeVar('R')  # Result type

def create_lazy_pipeline(
    creator: Callable[[], Callable[[T], R]]
) -> Callable[[T], R]:
    """Create a lazy-loaded pipeline with caching."""
    
    @lru_cache(maxsize=1)
    def get_pipeline() -> Callable[[T], R]:
        return creator()
    
    def pipeline(input_data: T) -> R:
        return get_pipeline()(input_data)
    
    return pipeline

# Create lazy-loaded pipelines
process_receipt = create_lazy_pipeline(
    lambda: create_vision_pipeline()
)

classify_receipt_products = create_lazy_pipeline(
    lambda: create_classification_pipeline()
)


import requests
from PIL import Image
import io

# URL of the image to download
image_url = "https://i.ibb.co/rZR6JrX/image.jpg"  # Replace with your image URL

# Step 1: Download the image from the internet using requests
response = requests.get(image_url)
response.raise_for_status()  # Raise an error if the download fails

def resize_and_compress_image(response):
    image_bytes = io.BytesIO(response.content)
    image = Image.open(image_bytes)

    # Resize the image while maintaining the aspect ratio
    desired_width = 800
    aspect_ratio = image.height / image.width
    new_height = int(desired_width * aspect_ratio)
    resized_image = image.resize((desired_width, new_height))

    # Compress the image
    encoded_image_bytes = io.BytesIO()
    resized_image.save(encoded_image_bytes, format=image.format, quality=90)
    image_bytes = encoded_image_bytes.getvalue()

    return image_bytes

image_bytes = resize_and_compress_image(response)

# Step 4: Use the image bytes with process_receipt
print("AI Container")
result = process_receipt(image_bytes)

# Step 5: Print the results
print(result.data)
print(result.success)
print(result.error)
