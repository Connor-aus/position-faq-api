# src/utils/logger.py
import structlog
from dotenv import load_dotenv
import os

load_dotenv()
logging_level = os.getenv("LOGGING_LEVEL", "20")

print(f"Logging level: {logging_level}")

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(10),
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
)

log = structlog.get_logger()