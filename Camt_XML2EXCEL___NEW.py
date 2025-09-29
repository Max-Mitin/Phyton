import pandas as pd
import re
import pdfplumber

def read_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def process_text(text):
    # Разделим текст на отдельные выписки
    statements = text.split('АО "Банк ДОМ.РФ"')
    
    data = []
    
    for statement in statements:
        if statement.strip():  # Пропускаем пустые строки
            # Ищем номер счета
            account_match = re.search(r'Счет.*?(\d{20})', statement)
            # Ищем исходящий остаток, учитывая формат с разделителями
            balance_match = re.search(r'ИСХОДЯЩИЙ ОСТАТОК.*?(\d+(?:,\d{3})*(?:\.\d{2})?)', statement)
            
            if account_match and balance_match:
                account = account_match.group(1)
                # Удаляем запятые из числа и преобразуем в float
                balance = float(balance_match.group(1).replace(',', ''))
                
                data.append({
                    'Номер счета': account,
                    'Исходящий остаток': balance
                })
    
    # Создаем DataFrame
    df = pd.DataFrame(data)
    
    if not df.empty:
        # Сортируем по исходящему остатку по убыванию
        df = df.sort_values('Исходящий остаток', ascending=False)
        
        # Форматируем номер счета как строку с ведущими нулями
        df['Номер счета'] = df['Номер счета'].astype(str).str.zfill(20)
        
        # Форматируем исходящий остаток с разделителями тысяч и двумя знаками после запятой
        df['Исходящий остаток'] = df['Исходящий остаток'].apply(lambda x: '{:,.2f}'.format(x))
    else:
        print("Предупреждение: Не найдено данных для обработки")
    
    return df

# Путь к вашему файлу
pdf_path = 'report - 2025-02-18T155504.351.pdf'

# Читаем PDF и получаем текст
text = read_pdf(pdf_path)

# Обрабатываем текст
df = process_text(text)

if not df.empty:
    # Сохраняем в Excel с специальными настройками
    writer = pd.ExcelWriter('bank_statements.xlsx', engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Выписки')
    
    # Получаем объект workbook и worksheet
    workbook = writer.book
    worksheet = writer.sheets['Выписки']
    
    # Форматирование для номера счета (как текст)
    account_format = workbook.add_format({'num_format': '@'})
    worksheet.set_column('A:A', 25, account_format)
    
    # Форматирование для суммы (с разделителями тысяч и двумя знаками после запятой)
    amount_format = workbook.add_format({'num_format': '#,##0.00'})
    worksheet.set_column('B:B', 20, amount_format)
    
    writer.close()
    
    print("Данные сохранены в файл 'bank_statements.xlsx'")
    print("\nПервые 5 записей:")
    print(df.head())
else:
    print("Ошибка: Не удалось извлечь данные из текста")
