### ЗДЕСЬ ЭКСПЕРИМЕНТЫ
import requests
from PIL import Image
import io
from logger import logger
from pipelines import process_receipt

# URL of the image to download
image_url = "https://i.ibb.co/rZR6JrX/image.jpg"  # Replace with your image URL

# Step 1: Download the image from the internet using requests
response = requests.get(image_url)
response.raise_for_status()  # Raise an error if the download fails

def resize_and_compress_image(response):
    image_bytes = io.BytesIO(response.content)
    image = Image.open(image_bytes)

    # Resize the image while maintaining the aspect ratio
    desired_width = 1120
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
logger.info("AI Container before process_receipt")
result = process_receipt(image_bytes)

# Step 5: Print the results
logger.debug(result.data)
logger.debug(result.success)
logger.debug(result.error)
