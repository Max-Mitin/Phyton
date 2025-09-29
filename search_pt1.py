import os
import shutil

# Путь к текстовому файлу со списком паспортов
passport_list_path = r"C:\2NDFL\export\for_script\part_3_er_up.txt"

# Путь к папке с файлами
files_path = r"C:\2NDFL\export\pdf"

# Путь к папке, куда нужно скопировать найденные файлы
destination_path = r"C:\2NDFL\export\pdf\sign\part_2_pp_er_upl"

# Создание папки, если она не существует
#os.makedirs(destination_path, exist_ok=True)

# Чтение списка паспортов из текстового файла
with open(passport_list_path, 'r', encoding='utf-8') as file:
    passport_numbers = [line.strip() for line in file]

# Проверка чтения паспортов
print("Список паспортов:")
for passport in passport_numbers:
    print(passport)

# Поиск и копирование найденных файлов
for passport in passport_numbers:
    pattern = f"{passport}.pdf"
    print(f"Поиск файлов с шаблоном: {pattern}")
    found_files = [f for f in os.listdir(files_path) if f.startswith(passport) and f.endswith('.pdf')]
    print(f"Найдено файлов: {len(found_files)} для паспорта {passport}")
    for file_name in found_files:
        source_file = os.path.join(files_path, file_name)
        destination_file = os.path.join(destination_path, file_name)
        shutil.copy2(source_file, destination_file)
        print(f"Скопирован файл: {source_file} в {destination_file}")
