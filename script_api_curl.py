import json
import pprint
import subprocess
import sys

from config import settings


def get_token_via_curl() -> str:
    """
    Получает OAuth токен через выполнение curl команды в shell.
    
    Returns:
        Access token строка
        
    Raises:
        SystemExit: Если не удалось получить токен
    """
    curl_command = [
        "curl",
        "-k",  # Пропустить проверку SSL сертификата (эквивалент verify=False в requests)
        "-L",
        "-X", "POST",
        settings.gigachat_oauth_url,
        "-H", "Content-Type: application/x-www-form-urlencoded",
        "-H", "Accept: application/json",
        "-H", f"RqUID: {settings.gigachat_client_id}",
        "-H", f"Authorization: Basic {settings.gigachat_client_secret}",
        "--data-urlencode", f"scope={settings.gigachat_scope}",
    ]
    
    try:
        result = subprocess.run(
            curl_command,
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            print(f"Ошибка выполнения curl: {result.stderr}", file=sys.stderr)
            sys.exit(1)
        
        response_data = json.loads(result.stdout)
        access_token = response_data.get("access_token")
        
        if not access_token:
            print(f"Ошибка: access_token не найден в ответе: {result.stdout}", file=sys.stderr)
            sys.exit(1)
        
        return access_token
        
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON ответа: {e}", file=sys.stderr)
        print(f"Ответ сервера: {result.stdout}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при выполнении curl: {e}", file=sys.stderr)
        sys.exit(1)


def execute_prompt_via_curl(
    system_prompt: str,
    user_prompt: str,
    access_token: str,
    chat_completions_url=settings.gigachat_chat_completions_url,
) -> dict:
    """
    Выполняет промпт через curl команду в shell.
    
    Args:
        system_prompt: Системный промпт
        user_prompt: Пользовательский промпт
        access_token: Access token для авторизации
        chat_completions_url: URL для chat completions API
        
    Returns:
        Результат выполнения промпта (dict)
        
    Raises:
        SystemExit: Если не удалось выполнить запрос
    """
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
    
    payload_json = json.dumps(payload, ensure_ascii=False)
    
    curl_command = [
        "curl",
        "-k",  # Пропустить проверку SSL сертификата
        "-X", "POST",
        chat_completions_url,
        "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer {access_token}",
        "--data", payload_json,
        "--max-time", "60",  # Таймаут 60 секунд
        "--write-out", "\n%{http_code}",  # Добавить HTTP статус код в конец вывода
        "--silent",  # Не показывать прогресс
    ]
    
    try:
        result = subprocess.run(
            curl_command,
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            print(f"Ошибка выполнения curl: {result.stderr}", file=sys.stderr)
            sys.exit(1)
        
        # Разделяем тело ответа и HTTP статус код
        output_lines = result.stdout.strip().split('\n')
        if len(output_lines) < 2:
            # Если нет статус кода, пытаемся распарсить как есть
            response_data = json.loads(result.stdout)
        else:
            # Последняя строка - HTTP статус код
            http_status = output_lines[-1]
            response_body = '\n'.join(output_lines[:-1])
            
            # Проверяем HTTP статус код
            if not http_status.startswith('2'):
                # HTTP ошибка
                try:
                    error_data = json.loads(response_body)
                    error_msg = f"Ошибка API: {http_status} - {error_data.get('error', response_body)}"
                except json.JSONDecodeError:
                    error_msg = f"Ошибка API: {http_status} - {response_body}"
                print(error_msg, file=sys.stderr)
                sys.exit(1)
            
            response_data = json.loads(response_body)
        
        # Дополнительная проверка на наличие ошибок в JSON ответе
        if "error" in response_data:
            error_msg = f"Ошибка API: {response_data.get('error', 'Unknown error')}"
            print(error_msg, file=sys.stderr)
            sys.exit(1)
        
        return response_data
        
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON ответа: {e}", file=sys.stderr)
        print(f"Ответ сервера: {result.stdout}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при выполнении curl: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    system_prompt = "Ты мастер рассказывать анекдоты"
    user_prompt = "Придумай короткий анекдот про программиста"

    token = get_token_via_curl()
    print(token)
    result = execute_prompt_via_curl(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        access_token=token,
    )
    pprint.pprint(result)


if __name__ == "__main__":
    main()
