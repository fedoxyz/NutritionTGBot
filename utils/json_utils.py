import json
from logs.logger import logger
from datetime import datetime

def parse_json_file(file_content: bytes) -> dict:
    try:
        # Parse JSON data
        data = json.loads(file_content.decode('utf-8'))

        # Validate the JSON data structure
        validate_receipt_data(data)

        receipt_date_str = data.get("localDateTime")
        if receipt_date_str:
            # Parse the date string to a datetime object
            receipt_date = datetime.fromisoformat(receipt_date_str)
        else:
            # Fallback: convert Unix timestamp to datetime with timezone
            timestamp = data.get("dateTime")
            receipt_date = datetime.fromtimestamp(timestamp)

        # Extract product details
        products = [
                {   "id": int(i),
                "name": item["name"],
                "price": item["price"],
                "quantity": item["quantity"]
            }
            for i, item in enumerate(data.get("items", []))
        ]

        # Return the result dictionary
        return {
            "receipt_date": receipt_date,
            "products": products
        }

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        logger.error(f"Error parsing JSON: {e}")
        return {}

def validate_receipt_data(json_data: dict) -> None:
    """Ensure required keys are present and items list is not empty."""
    required_keys = ["items"]

    # Check for required keys
    if not all(key in json_data for key in required_keys):
        raise ValueError("Missing required keys in JSON data")

    # Check that the items list is not empty
    if not json_data["items"]:
        raise ValueError("The 'items' list must contain at least one item")
