import pprint
from gigachat import GigaChat

from config import settings
from logger import logger


def main():
    system_prompt = "Ты мастер рассказывать анекдоты"
    user_prompt = "Придумай короткий анекдот про программиста"

    try:
        giga = GigaChat(credentials=settings.gigachat_client_secret)
        result = giga.chat({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        })
        pprint.pprint(result)
    except Exception as error:
        logger.error("Error with GigaChat: %s", error)


if __name__ == "__main__":
    main()
