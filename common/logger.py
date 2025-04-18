import logging

logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("code.challenge")

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(asctime)s %(message)s"
)
