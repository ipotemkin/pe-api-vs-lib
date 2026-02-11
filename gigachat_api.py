"""Модуль для работы с GigaChat API."""
import requests

from config import settings
from logger import logger


class GigaChatError(Exception):
    """Базовое исключение для ошибок GigaChat API."""

    pass


class AuthenticationError(GigaChatError):
    """Ошибка аутентификации."""

    pass


class APIError(GigaChatError):
    """Ошибка API запроса."""

    pass


def get_access_token(client_id: str, client_secret: str, oauth_url: str) -> str:
    """
    Получает OAuth токен для доступа к GigaChat API.
    
    Args:
        client_id: Client ID из учетных данных
        client_secret: Client Secret из учетных данных
        oauth_url: URL для OAuth аутентификации
        
    Returns:
        Access token строка
        
    Raises:
        AuthenticationError: Если не удалось получить токен
    """
    logger.info("Получение access token...")
        
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": client_id,
        "Authorization": f"Basic {client_secret}",
    }
    
    data = {
        "scope": settings.gigachat_scope,
    }
    
    try:
        response = requests.post(
            oauth_url,
            headers=headers,
            data=data,
            timeout=30,
        )
        
        if response.status_code != 200:
            error_msg = f"Ошибка аутентификации: {response.status_code} - {response.text}"
            logger.error(error_msg)
            raise AuthenticationError(error_msg)
        
        token_data = response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            error_msg = "Access token не найден в ответе"
            logger.error(error_msg)
            raise AuthenticationError(error_msg)
        
        logger.info("Access token успешно получен")
        return access_token
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Ошибка при запросе токена: {str(e)}"
        logger.error(error_msg)
        raise AuthenticationError(error_msg) from e


def execute_prompt(system_prompt: str, user_prompt: str, access_token: str, chat_completions_url: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    
    payload = {
        "model": "GigaChat",
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ]
    }
    
    try:
        response = requests.post(
            chat_completions_url,
            headers=headers,
            json=payload,
            timeout=60,
        )
        
        if response.status_code != 200:
            error_msg = f"Ошибка API: {response.status_code} - {response.text}"
            logger.error(error_msg)
            raise APIError(error_msg)
        
        result = response.json()
        return result
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Ошибка при запросе к API: {str(e)}"
        logger.error(error_msg)
        raise APIError(error_msg) from e
