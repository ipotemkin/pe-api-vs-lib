#!/bin/bash

# Скрипт для получения OAuth токена GigaChat через curl
# Переменные загружаются из .env файла

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "Ошибка: файл .env не найден" >&2
    exit 1
fi

# Загрузка переменных из .env
# Используем set -a для автоматического экспорта переменных
set -a
source .env
set +a

# Проверка наличия обязательных переменных
if [ -z "$gigachat_oauth_url" ]; then
    gigachat_oauth_url="https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
fi

if [ -z "$GIGACHAT_SCOPE" ]; then
    GIGACHAT_SCOPE="GIGACHAT_API_PERS"
fi

if [ -z "$GIGACHAT_CLIENT_ID" ]; then
    echo "Ошибка: переменная GIGACHAT_CLIENT_ID не установлена в .env" >&2
    exit 1
fi

if [ -z "$GIGACHAT_CLIENT_SECRET" ]; then
    echo "Ошибка: переменная GIGACHAT_CLIENT_SECRET не установлена в .env" >&2
    exit 1
fi

# Выполнение curl запроса для получения токена
# Сохраняем stdout и stderr отдельно, а также HTTP статус код
http_code=$(curl -L -w "\n%{http_code}" -X POST \
    "$gigachat_oauth_url" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept: application/json" \
    -H "RqUID: $GIGACHAT_CLIENT_ID" \
    -H "Authorization: Basic $GIGACHAT_CLIENT_SECRET" \
    --data-urlencode "scope=$GIGACHAT_SCOPE" \
    2>&1)

curl_exit_code=$?

# Разделяем ответ и HTTP статус код
response=$(echo "$http_code" | head -n -1)
http_status=$(echo "$http_code" | tail -n 1)

# Проверка успешности выполнения curl
if [ $curl_exit_code -ne 0 ]; then
    echo "Ошибка выполнения curl запроса (код выхода: $curl_exit_code)" >&2
    echo "Полный вывод curl:" >&2
    echo "$http_code" >&2
    exit 1
fi

# Проверка HTTP статус кода
if [ -z "$http_status" ] || [ "$http_status" -lt 200 ] || [ "$http_status" -ge 300 ]; then
    echo "Ошибка HTTP: статус код $http_status" >&2
    echo "Полный ответ сервера:" >&2
    echo "$response" >&2
    exit 1
fi

# Извлечение access_token из JSON ответа
# Используем jq если доступен, иначе grep/sed
if command -v jq &> /dev/null; then
    access_token=$(echo "$response" | jq -r '.access_token // empty' 2>&1)
    jq_exit_code=$?
    if [ $jq_exit_code -ne 0 ]; then
        echo "Ошибка парсинга JSON с помощью jq (код выхода: $jq_exit_code)" >&2
        echo "Ответ сервера:" >&2
        echo "$response" >&2
        exit 1
    fi
else
    # Fallback на grep/sed если jq не установлен
    access_token=$(echo "$response" | grep -o '"access_token"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"access_token"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/' 2>&1)
fi

# Проверка наличия токена
if [ -z "$access_token" ] || [ "$access_token" = "null" ] || [ "$access_token" = "empty" ]; then
    echo "Ошибка: access_token не найден в ответе" >&2
    echo "HTTP статус: $http_status" >&2
    echo "Полный ответ сервера:" >&2
    echo "$response" >&2
    
    # Попытка извлечь информацию об ошибке из JSON, если она есть
    if command -v jq &> /dev/null; then
        error_info=$(echo "$response" | jq -r '.error // .message // empty' 2>/dev/null)
        if [ -n "$error_info" ] && [ "$error_info" != "null" ]; then
            echo "Информация об ошибке из ответа: $error_info" >&2
        fi
    fi
    
    exit 1
fi

# Вывод токена
echo "$access_token"
