import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Регистрация шрифта для кириллицы
outpath = os.path.join(os.getcwd(), 'font')
pdfmetrics.registerFont(TTFont('DejaVuSans', os.path.join(outpath, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', os.path.join(outpath, 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSerif', os.path.join(outpath, 'DejaVuSerif.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', os.path.join(outpath, 'DejaVuSerif-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Italic', os.path.join(outpath, 'DejaVuSerif-Italic.ttf')))
font_path = "DejaVuSans.ttf"
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont('DejaVu', font_path))
    pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'DejaVuSans-Bold.ttf' if os.path.exists('DejaVuSans-Bold.ttf') else font_path))
else:
    # Если шрифт не найден, используем стандартный
    pdfmetrics.registerFont(TTFont('DejaVu', 'Helvetica'))

# Размеры страницы A4 (книжная)
page_size = A4
width, height = page_size

# Параметры сетки
cols = 32
rows = 31
col_width = 5.5 * mm  # ширина колонки (~5.2 мм для 32 колонок на A4)
row_height = 4 * mm    # высота строки

# Функция создания одного бегунка
def create_begunok():
    """Создает таблицу-бегунок по точной копии из Excel"""
    
    # Подготовка данных (31 строка x 32 колонки)
    data = []
    
    # Строка 0: Министерство спорта
    row0 = [""] * cols
    row0[0] = "Министерство спорта Российской Федерации"
    data.append(row0)
    
    # Строка 1: Федерация
    row1 = [""] * cols
    row1[0] = "Общероссийская физкультурно-спортивная общественная организация «Федерация настольного тенниса России»"
    data.append(row1)
    
    # Строка 2: Федерация (продолжение)
    row2 = [""] * cols
    row2[0] = ""
    data.append(row2)
    
    # Строка 3: Протокол
    row3 = [""] * cols
    row3[0] = "Протокол одиночной встречи"
    row3[23] = "Дата"
    data.append(row3)
    
    # Строка 4: =[1]Список!A1
    row4 = [""] * cols
    row4[0] = "ВСЕРОССИЙСКИЕ СОРЕВНОВАНИЯ ПО НАСТОЛЬНОМУ ТЕННИСУ"
    row4[23] = "Время"
    data.append(row4)
    
    # Строка 5: =[1]Список!A2
    row5 = [""] * cols
    row5[0] = "Надежды России"
    row5[23] = "Стол"
    data.append(row5)
    
    # Строка 6: =[1]Список!A3
    row6 = [""] * cols
    row6[0] = "=[1]Список!A3"
    row6[23] = "Стадия"
    data.append(row6)
    
    # Строка 7: пустая + Матч №
    row7 = [""] * cols
    row7[23] = "Матч №"
    data.append(row7)
    
    # Строка 8: пустая
    row8 = [""] * cols
    data.append(row8)
    
    # Строка 9: Ф.И.О. участников ... (заголовки таблицы)
    row9 = [""] * cols
    row9[0] = "Ф.И.О. участников"
    row9[8] = "Рейтинг"
    row9[11] = "Субъект РФ"
    row9[16] = "П"
    row9[17] = "П1"
    row9[18] = "П2"
    row9[19] = "Счет в партиях"
    row9[28] = "Общий счет партий"
    data.append(row9)
    
    # Строка 10: номера партий
    row10 = [""] * cols
    row10[19] = "1"
    row10[21] = "2"
    row10[23] = "3"
    row10[25] = "4"
    row10[27] = "5"
    data.append(row10)
    
    # Строки 11-12: пустые (для участников)
    row11 = [""] * cols
    data.append(row11)
    row12 = [""] * cols
    data.append(row12)
    
    # Строка 13: пустая
    row13 = [""] * cols
    data.append(row13)
    
    # Строка 14: Победил(а)
    row14 = [""] * cols
    row14[0] = "Победил(а)"
    row14[13] = "Со счетом"
    data.append(row14)
    
    # Строки 15-16: пустые
    row15 = [""] * cols
    data.append(row15)
    row16 = [""] * cols
    data.append(row16)
    
    # Строка 17: Тренер
    row17 = [""] * cols
    row17[0] = "Тренер (секундант) участника"
    data.append(row17)
    
    # Строки 18-20: пустые
    for _ in range(3):
        data.append([""] * cols)
    
    # Строка 21: Ф.И.О. судей
    row21 = [""] * cols
    row21[0] = "Ф.И.О. судей"
    row21[16] = "Подписи судей"
    data.append(row21)
    
    # Строки 22-24: пустые
    for _ in range(3):
        data.append([""] * cols)
    
    # Строка 25: Сокращение в таблицах
    row25 = [""] * cols
    row25[0] = "Сокращение в таблицах:"
    row25[22] = "Контрольные отметки ГСК"
    data.append(row25)
    
    # Строка 26: пустая
    row26 = [""] * cols
    data.append(row26)
    
    # Строка 27: П - предупреждение
    row27 = [""] * cols
    row27[2] = "П -"
    row27[3] = "предупреждение"
    row27[22] = "1"
    row27[27] = "2"
    data.append(row27)
    
    # Строка 28: подписи
    row28 = [""] * cols
    row28[22] = "(Зам. главного судьи)"
    row28[27] = "(Зам. главного секретаря)"
    data.append(row28)
    
    # Строка 29: П1 - одно штрафное очко
    row29 = [""] * cols
    row29[2] = "П1 -"
    row29[3] = "одно штрафное очко"
    data.append(row29)
    
    # Строка 30: П2 - два штрафных очка
    row30 = [""] * cols
    row30[2] = "П2 -"
    row30[3] = "два штрафных очка"
    data.append(row30)
    
    # Создание таблицы с точными размерами колонок
    col_widths = [col_width] * cols
    
    table = Table(data, colWidths=col_widths, rowHeights=[row_height] * rows)

    # fn = ('BOX', (23, 3), (31, 7), 1, colors.darkblue)
    # style.append(fn) 
    # ts = style   # стиль таблицы (список оформления строк и шрифта)
    # Стиль таблицы - точная копия всех линий
    style = [
        # Все линии сетки - черные, тонкие
        ('GRID', (0, 0), (-1, -1), 0.2, colors.lightgrey),
        
        # Основной шрифт
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu'),
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('LEADING', (0, 0), (-1, -1), 7),
        
        # Выравнивание
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        
        # Отступы
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
        ('RIGHTPADDING', (0, 0), (-1, -1), 1),
        
        # Объединение ячеек для заголовков
        ('SPAN', (0, 9), (7, 10)),  # Ф.И.О. участников (колонки 0-7)
        ('SPAN', (8, 9), (10, 9)),  # Рейтинг (колонки 8-10)
        ('SPAN', (11, 9), (15, 9)),  # Субъект РФ (колонки 11-15)
        ('SPAN', (19, 9), (27, 9)),  # Счет в партиях (колонки 19-27)
        
        # Жирный шрифт для заголовков
        # ('FONTNAME', (0, 9), (-1, 9), 'DejaVu-Bold'),
        ('FONTNAME', (0, 0), (0, 2), 'DejaVu-Bold'),  # Министерство и федерация
        ('FONTNAME', (0, 3), (20, 3), 'DejaVu-Bold'),  # Протокол
        
        # Центрирование некоторых заголовков
        ('ALIGN', (0, 0), (31, 0), 'CENTER'),  # минспорта
        ('ALIGN', (0, 1), (31, 1), 'CENTER'),  # ФНТР
        ('ALIGN', (0, 3), (20, 3), 'CENTER'),  # Протокол
        ('ALIGN', (0, 4), (20, 4), 'CENTER'),  # соревнования
        ('ALIGN', (0, 5), (20, 5), 'CENTER'),  # название
        ('ALIGN', (8, 9), (10, 9), 'CENTER'),  # Рейтинг
        ('ALIGN', (16, 9), (18, 9), 'CENTER'),  # П, П1, П2
        ('ALIGN', (19, 10), (27, 10), 'CENTER'),  # Номера партий
        ('ALIGN', (28, 9), (31, 9), 'CENTER'),  # Общий счет
        
        # Специальные объединения
        ('SPAN', (0, 0), (31, 0)),  # Министерство спорта
        ('SPAN', (0, 1), (31, 1)),  # Федерация (часть 1)
        ('SPAN', (0, 2), (22, 2)),  # Федерация (часть 2)
        ('SPAN', (0, 3), (20, 3)),  # Протокол
        ('SPAN', (0, 4), (20, 4)),  # =[1]Список!A1
        ('SPAN', (0, 5), (20, 5)),  # =[1]Список!A2
        ('SPAN', (0, 6), (20, 6)),  # =[1]Список!A3

        
        # == блок фио, рейтинг, ввод счета
        ('SPAN', (0, 11), (7, 11)),  # заголовок ФИО
        ('SPAN', (0, 12), (7, 12)),  # поле фио
        ('SPAN', (8, 9), (10, 10)),  # заголовок рейтинг
        ('SPAN', (8, 11), (10, 11)),  # поле рейтинг
        ('SPAN', (8, 12), (10, 12)),  # поле рейтинг
        ('SPAN', (11, 9), (15, 10)), # заголовок субъекты столбцы от 0 до 7, строки 9-10
        ('SPAN', (11, 11), (15, 11)), # поле субъекты столбцы от 0 до 7, строки 9-10
        ('SPAN', (11, 12), (15, 12)), # поле субъекты столбцы от 0 до 7, строки 9-10
        # ('SPAN', (28, 7), (31, 7)),  # Матч №
        ('BOX', (0, 9), (7, 10), 1, colors.darkblue), # столбцы от 0 до 7, строки 9-10
        ('BOX', (0, 11), (7, 11), 1, colors.darkblue), # столбцы от 0 до 7, строки 9-10
        ('BOX', (0, 12), (7, 12), 1, colors.darkblue), # столбцы от 0 до 7, строки 9-10
        ('BOX', (8, 9), (10, 10), 1, colors.darkblue), # столбцы от 0 до 7, строки 9-10 рейтинг
        ('BOX', (11, 9), (15, 10), 1, colors.darkblue), # столбцы от 0 до 7, строки 9-10 субъекты
        # Победитель
        ('SPAN', (0, 14), (10, 14)),  # Победил(а)
        ('SPAN', (13, 14), (17, 14)),  # Со счетом
        
        # Тренер
        ('SPAN', (0, 17), (15, 17)),  # Тренер
        
        # Судьи
        ('SPAN', (0, 21), (15, 21)),  # Ф.И.О. судей
        ('SPAN', (16, 21), (31, 21)),  # Подписи судей
        
        # Сокращения
        ('SPAN', (0, 25), (12, 25)),  # Сокращение в таблицах:
        ('SPAN', (22, 25), (31, 25)),  # Контрольные отметки ГСК
        ('SPAN', (22, 27), (26, 27)),  # 1
        ('SPAN', (27, 27), (31, 27)),  # 2
        ('SPAN', (22, 28), (26, 28)),  # (Зам. главного судьи)
        ('SPAN', (27, 28), (31, 28)),  # (Зам. главного секретаря)
    ]   
    # === блок ввода даты, номер стола встречи и т.д.
    for i in range(0, 5): 
        fn = ('SPAN', (23, 3 + i), (27, 3 + i))
        style.append(fn)  # Дата
        fn = ('SPAN', (28, 3 + i), (31, 3 + i))
        style.append(fn)  # Дата
        fn = ('BOX', (23, 3 + i), (27, 3 + i), 1, colors.darkblue)
        style.append(fn)
        fn = ('BOX', (27, 3 + i), (31, 3 + i), 1, colors.darkblue) # рисует внешние границы
        style.append(fn)
        fn =  ('BACKGROUND', (23, 3 + i), (27, 3 + i), colors.lightyellow)
        style.append(fn)
        fn = ('ALIGN', (23, 3 + i), (27, 3 + i), 'CENTER')  # минспорта
        style.append(fn)
        fn = ('FONTNAME', (23, 3 + i), (27, 3 + i), 'DejaVuSerif-Italic')  # минспорта
        style.append(fn)
        fn = ('FONTSIZE', (23, 3 + i), (27, 3 + i), 10)  # минспорта
        style.append(fn)
    # ========  
    # for i in range(0, 2):
    ('BOX', (0, 9), (1, 15), 1, colors.darkblue)

        # style.append(fn)  # ФИО  

    table.setStyle(TableStyle(style))
    
    return table

# Создание PDF
c = canvas.Canvas("Begunki_2.pdf", pagesize=page_size)

# Создаем таблицу-бегунок
begunok = create_begunok()

# Рассчитываем размеры таблицы
table_width = cols * col_width
table_height = rows * row_height

# Позиции для двух бегунков
margin = 5 * mm
vertical_spacing = 10 * mm

# Верхний бегунок
x1 = margin
y1 = height - margin - table_height
begunok.wrapOn(c, table_width, table_height)
begunok.drawOn(c, x1, y1)

# Нижний бегунок
x2 = margin
y2 = y1 - table_height - vertical_spacing
begunok.wrapOn(c, table_width, table_height)
begunok.drawOn(c, x2, y2)

# Добавляем разделительную линию между бегунками
c.setStrokeColorRGB(0.7, 0.7, 0.7)
c.setLineWidth(0.2)
c.line(margin, y2 + table_height + vertical_spacing/2, 
       margin + table_width, y2 + table_height + vertical_spacing/2)

# Добавляем подписи
c.setFont('DejaVu', 7)
c.drawString(margin, y1 + table_height + 2*mm, "Бегунок 1")
c.drawString(margin, y2 + table_height + 2*mm, "Бегунок 2")

c.save()

print("PDF 'Begunki_2.pdf' успешно создан!")
print(f"Размер страницы: {width/10:.0f} x {height/10:.0f} мм")
print(f"Размер одного бегунка: {table_width/10:.1f} x {table_height/10:.1f} мм")
print(f"Сетка: {cols} колонок x {rows} строк")