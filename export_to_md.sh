#!/bin/bash

# Вы можете переименовать этот файл во что-то вроде export_myquartapp_to_md.sh

# Укажите путь к проекту (my_quart_app). ОБЯЗАТЕЛЬНО в кавычках!
PROJECT_DIR="/Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app"

# Название выходного .md-файла
OUTPUT_FILE="project_structure_myquartapp.md"

# 1. Выводим заголовок и дерево каталогов (пропускаем venv, .venv, __pycache__, .git)
echo "# Project Structure" > "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
tree "$PROJECT_DIR" -I "venv|\.venv|__pycache__|\.git" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 2. Заголовок для исходного кода
echo "# Source Code" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 3. Находим файлы с расширением .py, исключая виртуальные окружения/кэши
find "$PROJECT_DIR" \
  -path "*/venv/*" -prune -o \
  -path "*/.venv/*" -prune -o \
  -path "*/__pycache__/*" -prune -o \
  -path "*/.git/*" -prune -o \
  -name "*.py" -print |
while read file; do
  echo "## $file" >> "$OUTPUT_FILE"
  echo '```python' >> "$OUTPUT_FILE"
  cat "$file" >> "$OUTPUT_FILE"
  echo '```' >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
done

echo "Done. Created $OUTPUT_FILE."