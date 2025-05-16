# College Helper Bot

Бот-помощник для колледжа, включающий напоминания, функцию отслеживания посещаемости и автоматические обновления.

### Подготовка окружения



### Требования

- Python 3.10+
- Библиотеки:
    - aiogram
    - python-dotenv
    - pydantic-settings
    - pymysql
    - apscheduler
    - pandas
    - openpyxl
    - pillow

## Подготовка окружения

### Настройке конфигурации

Создайте .env файл в корневой директории и заполните следующими переменными:

```
BOT_TOKEN=your_telegram_bot_token_here
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
```

В файле config.py укажите id телеграм группы:

```
TELEGRAM_GROUP: str = "-10022959691"
```

### Установка зависимостей

Перейдите в корневую папку:
```
cd college-bot
```

Установите **poetry** и зависимости:
```
pip install poetry
poetry install
```

### Запуск

Выдайте права файлу запуска:
```
cd scripts
chmod +x ./start_bot.sh
```

Запустите бота:
```
./start_bot.sh
```
