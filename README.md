# Postman API Library для GigaChat

Библиотека для работы с GigaChat API через различные методы: HTTP запросы (requests), curl команды и официальный SDK.

## Требования

- Python 3.11+
- curl (для скриптов с использованием curl)

## Установка

1. Клонируйте репозиторий или скачайте проект

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
# или
venv\Scripts\activate  # Для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Настройка

### 1. Создайте файл `.env`

Скопируйте файл `.env.example` в `.env` и заполните его своими данными:

```bash
cp .env.example .env
```

Затем откройте файл `.env` и укажите ваши учетные данные:

```env
GIGACHAT_CLIENT_ID=your_client_id
GIGACHAT_CLIENT_SECRET=your_client_secret
GIGACHAT_SCOPE=GIGACHAT_API_PERS
```

Где:
- `GIGACHAT_CLIENT_ID` - ваш Client ID из учетных данных GigaChat API
- `GIGACHAT_CLIENT_SECRET` - ваш Client Secret из учетных данных GigaChat API
- `GIGACHAT_SCOPE` - область доступа (по умолчанию: `GIGACHAT_API_PERS`)

### 2. Установка сертификатов Минцифры

**⚠️ ВАЖНО:** Для работы с GigaChat API необходимо установить корневой сертификат Минцифры. Без него при попытке получить токен доступа будет возвращаться ошибка валидации сертификата:

```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain
```

#### Установка на уровне приложения (рекомендуется)

Для автоматической установки сертификатов выполните команду:

```bash
curl -k "https://gu-st.ru/content/lending/russian_trusted_root_ca_pem.crt" -w "\n" >> $(python -m certifi)
```

При выполнении команды сертификат скачивается и устанавливается автоматически. При переходе в новую виртуальную среду может понадобиться повторная установка сертификата.

#### Установка на уровне ОС

Подробные инструкции по установке сертификатов на уровне операционной системы для разных платформ (Windows, macOS, Linux) доступны в [официальной документации GigaChat](https://developers.sber.ru/docs/ru/gigachat/certificates).

#### Альтернативный способ для библиотеки gigachat

Если вы используете библиотеку `gigachat`, вы можете указать путь к файлу сертификата в параметре `ca_bundle_file` при инициализации:

```python
from gigachat import GigaChat

giga = GigaChat(
   credentials="ключ_авторизации",
   scope="GIGACHAT_API_PERS",
   model="GigaChat",
   ca_bundle_file="/путь/к/файлу/russian_trusted_root_ca_pem.crt"
)
```

## Использование

### script_api.py

Скрипт для работы с GigaChat API через библиотеку `requests`:

```bash
python script_api.py
```

Использует функции из модуля `gigachat_api.py` для получения токена и выполнения промптов.

### script_api_curl.py

Скрипт для работы с GigaChat API через выполнение `curl` команд в shell:

```bash
python script_api_curl.py
```

Включает функции:
- `get_token_via_curl()` - получение OAuth токена через curl
- `execute_prompt_via_curl()` - выполнение промпта через curl

### script_gigachat_lib.py

Скрипт для работы с GigaChat API через официальный SDK `gigachat`:

```bash
python script_gigachat_lib.py
```

## Структура проекта

```
postman-api-lib/
├── config.py              # Конфигурация на базе pydantic-settings
├── gigachat_api.py        # Модуль для работы с GigaChat API через requests
├── logger.py              # Настройка логирования
├── script_api.py          # Скрипт с использованием requests
├── script_api_curl.py     # Скрипт с использованием curl
├── script_gigachat_lib.py # Скрипт с использованием официального SDK
├── requirements.txt       # Зависимости проекта
└── README.md             # Документация
```

## Модули

### config.py

Модуль конфигурации на базе `pydantic-settings`. Автоматически загружает переменные окружения из файла `.env`.

Доступные настройки:
- `gigachat_client_id` - Client ID (обязательное)
- `gigachat_client_secret` - Client Secret (обязательное)
- `gigachat_scope` - Область доступа (по умолчанию: `GIGACHAT_API_PERS`)
- `gigachat_oauth_url` - URL для OAuth аутентификации
- `gigachat_chat_completions_url` - URL для chat completions API

### gigachat_api.py

Модуль с функциями для работы с GigaChat API:
- `get_access_token()` - получение OAuth токена
- `execute_prompt()` - выполнение промпта

## Дополнительная информация

- [Документация GigaChat API](https://developers.sber.ru/docs/ru/gigachat/)
- [Установка сертификатов Минцифры](https://developers.sber.ru/docs/ru/gigachat/certificates)

## Лицензия

Проект создан для образовательных целей.
