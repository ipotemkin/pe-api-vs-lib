import pprint

from gigachat_api import execute_prompt, get_access_token
from config import settings


def main():
    system_prompt = "Ты мастер рассказывать анекдоты"
    user_prompt = "Придумай короткий анекдот про программиста"

    token = get_access_token(
        settings.gigachat_client_id,
        settings.gigachat_client_secret,
        settings.gigachat_oauth_url
    )
    result = execute_prompt(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        access_token=token,
        chat_completions_url=settings.gigachat_chat_completions_url
    )
    pprint.pprint(result)


if __name__ == "__main__":
    main()