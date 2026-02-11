import os
import pprint
import sys

from gigachat_api import execute_prompt, get_access_token
from dotenv import load_dotenv

from logger import logger

load_dotenv()

GIGACHAT_CLIENT_ID = os.getenv("GIGACHAT_CLIENT_ID", None)
GIGACHAT_CLIENT_SECRET = os.getenv("GIGACHAT_CLIENT_SECRET", None)
if not any((GIGACHAT_CLIENT_ID, GIGACHAT_CLIENT_SECRET)):
    logger.error("No credetials provided. Exiting...")
    sys.exit(1)


def main():
    system_prompt = "Ты мастер рассказывать анекдоты"
    user_prompt = "Придумай короткий анекдот про программиста"

    token = get_access_token(GIGACHAT_CLIENT_ID, GIGACHAT_CLIENT_SECRET)
    result = execute_prompt(system_prompt=system_prompt, user_prompt=user_prompt, access_token=token)
    pprint.pprint(result)


if __name__ == "__main__":
    main()