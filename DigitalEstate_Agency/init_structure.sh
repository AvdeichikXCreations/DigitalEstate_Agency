#!/usr/bin/env bash

# Скрипт создания структуры "my_quart_app"

# Название создаваемой папки
PROJECT_DIR="my_quart_app"

# 1. Создаём корневую директорию проекта
mkdir -p "$PROJECT_DIR"

# Переходим в неё
cd "$PROJECT_DIR" || exit 1

# 2. Создаём файлы верхнего уровня
touch app.py
touch requirements.txt

# 3. Создаём директорию и файлы контроллеров
mkdir -p controllers
touch controllers/__init__.py
touch controllers/telegram_controller.py
touch controllers/umnico_controller.py
touch controllers/widget_controller.py
touch controllers/admin_controller.py
touch controllers/db_controller.py
touch controllers/tester_controller.py

# 4. Создаём директорию и файлы для core
mkdir -p core
touch core/llm_controller.py

# 5. Создаём директорию и файл для rag
mkdir -p rag
touch rag/rag_service.py

# 6. Сообщение пользователю
echo "Структура my_quart_app создана в каталоге: $(pwd)"