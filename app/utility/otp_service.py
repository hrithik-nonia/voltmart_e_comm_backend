import httpx
import os
from dotenv import load_dotenv
import secrets

load_dotenv()

async def send_otp_email(email: str, otp: str):

    payload = {
        "sender": {
            "name": os.getenv("BREVO_SENDER_NAME"),
            "email": os.getenv("BREVO_SENDER_EMAIL")
        },
        "to": [
            {
                "email": email
            }
        ],
        "subject": "Your VoltMart OTP",
        "htmlContent": f"""
            <h2>Verify your email</h2>
            <p>Your OTP is:</p>
            <h1>{otp}</h1>
            <p>This OTP will expire in 5 minutes.</p>
        """
    }

    headers = {
        "accept": "application/json",
        "api-key": os.getenv("BREVO_API_KEY"),
        "content-type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.brevo.com/v3/smtp/email",
            json=payload,
            headers=headers
        )

    response.raise_for_status()
    return response.json()
  
def generate_otp()->str | None:
  return str(secrets.randbelow(900000) + 100000)
  