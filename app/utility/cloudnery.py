import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

# Cloudinary configure karo
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_image(file_bytes: bytes, folder: str = "voltmart") -> str:
    """
    Image upload karo Cloudinary pe
    Return: image URL (string)
    """
    result = cloudinary.uploader.upload(
        file_bytes,
        folder=folder,        # Cloudinary mein folder
        resource_type="image"
    )
    return result["secure_url"]  # HTTPS URL return hoga