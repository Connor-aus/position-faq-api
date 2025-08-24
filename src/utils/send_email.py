import json
import re
from src.utils.logger import log

class Response:
    def __init__(self, statusCode: int = 500, body: str = "Unknown error"):
        self.statusCode = statusCode
        self.body = body

def send_email(email_content: str) -> Response:
    try:
        log.info(f"Attempting to send email. Parsing email content: {email_content}")

        email_content_json = json.loads(email_content)
        email = email_content_json.get("EMAIL")
        subject = email_content_json.get("SUBJECT")
        message = email_content_json.get("MESSAGE")

        log.info(f"Successfully parsed email content. Email: {email}, Subject: {subject}, Message: {message}")

        # For local development, just log the email instead of sending it
        log.info(f"[LOCAL EMAIL] To: {email}, Subject: {subject}, Message: {message}")
        
        # Return a success response
        return Response(
            statusCode=200,
            body=json.dumps({
                "response": "Email logged locally (not sent in local development mode)"
            })
        )

    except Exception as e:
        log.error(f"Error processing email: {e}")
        return Response(
            statusCode=500,
            body=json.dumps({
                "response": "Internal server error"
            })
        )

# Optional: clean up parse_error_response if unused
def parse_error_response(response: dict) -> str:
    try:
        match = re.search(r'Value error, (.*?) \[type=value', response.get("error", ""))
        if match:
            return match.group(1)
    except Exception:
        pass
    return "Unknown error"