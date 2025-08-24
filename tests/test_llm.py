import env_setup
from src.llms.llm import llm
from src.utils.logger import log

import os
from dotenv import load_dotenv

load_dotenv()

log.debug("ANTHROPIC_API_KEY: " + os.getenv("ANTHROPIC_API_KEY"))

question = "Hello"
response = llm.invoke({"input": question})

log.debug("Response:")
log.debug(response)