# from reportlab.lib.pagesizes import A4, landscape
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak, Spacer
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib import colors
# from reportlab.lib.units import mm
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont

# class TwoTableDocument:
#     def __init__(self, filename):
#         self.filename = filename
#         self.doc = SimpleDocTemplate(
#             filename,
#             pagesize=landscape(A4),
#             topMargin=15*mm,
#             bottomMargin=15*mm,
#             leftMargin=10*mm,
#             rightMargin=10*mm
#             )
#         self.styles = getSampleStyleSheet()
#         self.elements = []

#         # Создаем кастомные стили
#         self.title_style = ParagraphStyle(
#             'TableTitle',
#             parent=self.styles['Heading2'],
#             fontSize=14,
#             textColor=colors.darkblue,
#             spaceAfter=6*mm,
#             alignment=1 # Центрирование
#             )

#         self.small_title_style = ParagraphStyle(
#             'SmallTableTitle',
#             parent=self.styles['Heading3'],
#             fontSize=12,
#             textColor=colors.darkgreen,
#             spaceAfter=4*mm,
#             alignment=1
#             )

#     def create_table_style(self, header_color=colors.HexColor('#4F81BD')):
#         """Создает стиль для таблицы"""
#         return TableStyle([
#             # Заголовок таблицы
#             ('BACKGROUND', (0, 0), (-1, 0), header_color),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#             ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('FONTSIZE', (0, 0), (-1, 0), 11),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 8),

#             # Тело таблицы
#             ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#DCE6F1')),
#             ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#             ('FONTSIZE', (0, 1), (-1, -1), 9),
#             ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
#             ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#EAF1DD')]),
#             ])

#     def generate_sample_data(self, num_records=50):
#         """Генерирует пример данных для демонстрации"""
#         left_data = [['ID', 'Наименование товара', 'Категория', 'Цена', 'Остаток']]
#         right_data = [['ID', 'Сотрудник', 'Отдел', 'Продажи', 'Бонус']]

#         categories = ['Электроника', 'Одежда', 'Книги', 'Спорт', 'Дом']
#         departments = ['IT', 'Маркетинг', 'Продажи', 'Финансы', 'HR']
#         names_left = ['Товар', 'Изделие', 'Продукт', 'Аксессуар']
#         names_right = ['Иванов', 'Петров', 'Сидоров', 'Кузнецов', 'Смирнов']

#         for i in range(1, num_records + 1):
#             # Данные для левой таблицы (товары)
#             left_data.append([i, f'{names_left[i % 4]} {i}', categories[i % 5], f'{i * 100:,} руб.'.replace(',', ' '),
#             i * 10
#             ])

#             # Данные для правой таблицы (сотрудники)
#             right_data.append([
#             i,
#             f'{names_right[i % 5]} А.{chr(65 + i % 3)}.',
#             departments[i % 5],
#             f'{i * 5000:,}'.replace(',', ' '),
#             f'{i * 500:,} руб.'.replace(',', ' ')
#             ])

#             return left_data, right_data

#     def create_tables_page(self, left_title, left_data, right_title, right_data,
#         left_col_widths=None, right_col_widths=None):
#         """Создает страницу с двумя таблицами"""

#         # Рассчитываем ширину колонок если не заданы
#         page_width = self.doc.width
#         table_width = (page_width - 20*mm) / 2 # минус отступы между таблицами

#         if not left_col_widths:
#             left_col_widths = [table_width * 0.15, table_width * 0.35,
#             table_width * 0.25, table_width * 0.15, table_width * 0.1]

#         if not right_col_widths:
#             right_col_widths = [table_width * 0.15, table_width * 0.3,
#             table_width * 0.2, table_width * 0.2, table_width * 0.15]

#             # Создаем таблицы
#             left_table = Table(left_data, colWidths=left_col_widths, repeatRows=1)
#             right_table = Table(right_data, colWidths=right_col_widths, repeatRows=1)

#             # Применяем стили
#             left_table.setStyle(self.create_table_style(colors.HexColor('#4F81BD'))) # Синий
#             right_table.setStyle(self.create_table_style(colors.HexColor('#8064A2'))) # Фиолетовый

#             # Создаем заголовки таблиц
#             left_title_para = Paragraph(left_title, self.title_style)
#             right_title_para = Paragraph(right_title, self.title_style)

#             # Создаем контейнер для двух таблиц в ряд
#             # Используем таблицу с двумя колонками для заголовков и таблиц
#             container_data = [
#                 [left_title_para, right_title_para],
#                 [left_table, right_table]
#                 ]

#             container = Table(container_data,
#                 colWidths=[table_width, table_width],
#                 rowHeights=[15*mm, None])

#             container.setStyle(TableStyle([
#                 ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#                 ('LEFTPADDING', (0, 0), (-1, -1), 5*mm),
#                 ('RIGHTPADDING', (0, 0), (-1, -1), 5*mm),
#                 ('BOTTOMPADDING', (0, 0), (-1, -1), 10*mm),
#                 ]))

#             return container

#     def build_document(self, data_chunks=None):
#         """Строит документ с несколькими страницами"""

#         if not data_chunks:
#             # Генерируем тестовые данные
#             left_data, right_data = self.generate_sample_data(100)

#             # Разбиваем данные на чанки для нескольких страниц
#             rows_per_page = 15 # Количество строк на странице
#             data_chunks = []

#             for i in range(0, len(left_data), rows_per_page):
#                 left_chunk = left_data[i:i + rows_per_page]
#                 right_chunk = right_data[i:i + rows_per_page]
#                 data_chunks.append((left_chunk, right_chunk))

#                 # Добавляем общий заголовок документа
#             main_title = Paragraph("ЕЖЕМЕСЯЧНЫЙ ОТЧЕТ ПО ПРОДАЖАМ И ТОВАРАМ",
#             self.styles['Heading1'])
#             self.elements.append(main_title)
#             self.elements.append(Spacer(1, 10*mm))

#             # Создаем страницы с таблицами
#             for page_num, (left_chunk, right_chunk) in enumerate(data_chunks, 1):
#                 if page_num > 1:
#                     self.elements.append(PageBreak())

#                     page_title = f"Страница {page_num} из {len(data_chunks)}"
#                     page_header = Paragraph(page_title, self.small_title_style)
#                     self.elements.append(page_header)
#                     self.elements.append(Spacer(1, 5*mm))

#                     table_container = self.create_tables_page(
#                         left_title="📦 КАТАЛОГ ТОВАРОВ",
#                         left_data=left_chunk,
#                         right_title="👥 ОТЧЕТ ПО СОТРУДНИКАМ",
#                         right_data=right_chunk
#                         )

#                     self.elements.append(table_container)

#                     # Генерируем PDF
#                     self.doc.build(self.elements)
#                     print(f"Документ создан: {self.filename}")

#     # Пример использования с кастомными данными
#     def create_custom_document():
#         doc = TwoTableDocument("custom_tables.pdf")

#         # Кастомные данные
#         left_data = [
#             ['ID', 'Проект', 'Статус', 'Срок'],
#             ['1', 'Веб-сайт', 'Завершен', '2024-01'],
#             ['2', 'Мобильное приложение', 'В работе', '2024-03'],
#             ['3', 'База данных', 'Планируется', '2024-06'],
#             ['4', 'API интеграция', 'В работе', '2024-04'],
#             ]

#         right_data = [
#             ['ID', 'Задача', 'Приоритет', 'Прогресс'],
#             ['1', 'Дизайн интерфейса', 'Высокий', '100%'],
#             ['2', 'Разработка backend', 'Средний', '75%'],
#             ['3', 'Тестирование', 'Высокий', '50%'],
#             ['4', 'Документация', 'Низкий', '25%'],
#             ]

#         # Собираем документ с одной страницей
#         doc.build_document([(left_data, right_data)])

#     # Пример с большим количеством данных
#     # def create_large_document():
#     #     doc = TwoTableDocument("large_report.pdf")

#     #     # Генерируем много данных для демонстрации многопоточности
#     #     left_data, right_data = doc.generate_sample_data(200)

#     #     # Разбиваем на страницы по 12 строк
#     #     rows_per_page = 12
#     #     data_chunks = []

#     #     for i in range(0, len(left_data), rows_per_page):
#     #         left_chunk = left_data[i:i + rows_per_page]
#     #         right_chunk = right_data[i:i + rows_per_page]
#     #         data_chunks.append((left_chunk, right_chunk))

#     #         doc.build_document(data_chunks)

#     if __name__ == "__main__":
#         # Создаем несколько примеров
#         create_custom_document()
#         # create_large_document()

#         # Простой пример
# simple_doc = TwoTableDocument("simple_example.pdf")
# simple_doc.build_document()
# ----------- код 3
# from reportlab.lib.pagesizes import A4, landscape
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import inch

# # Создаём документ с альбомной ориентацией
# doc = SimpleDocTemplate("tables_report.pdf", pagesize=landscape(A4), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)

# # Стили для текста
# styles = getSampleStyleSheet()

# # Данные для таблиц
# data1 = [
#     ["Заголовок 1", "", ""],
#     ["Столбец 1", "Столбец 2", "Столбец 3"],
#     ["Данные 1", "Данные 2", "Данные 3"],
#     ["Данные 4", "Данные 5", "Данные 6"],
#     ]

# data2 = [
#     ["Заголовок 2", "", ""],
#     ["Столбец A", "Столбец B", "Столбец C"],
#     ["Значение 1", "Значение 2", "Значение 3"],
#     ["Значение 4", "Значение 5", "Значение 6"],
#     ]

# # Создаём таблицы
# table1 = Table(data1, colWidths=[1.5*inch, 1.5*inch, 1.5*inch])
# table1.setStyle(TableStyle([
# ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
# ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
# ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
# ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
# ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
# ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
# ('GRID', (0, 0), (-1, -1), 1, colors.black),
# ]))

# table2 = Table(data2, colWidths=[1.5*inch, 1.5*inch, 1.5*inch])
# table2.setStyle(TableStyle([
# ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
# ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
# ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
# ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
# ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
# ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
# ('GRID', (0, 0), (-1, -1), 1, colors.black),
# ]))

# # Собираем элементы для документа
# story = []

# # Добавляем заголовок для первой таблицы
# story.append(Paragraph("Таблица 1", styles['Heading1']))
# story.append(Spacer(1, 0.25*inch))
# story.append(table1)
# story.append(Spacer(1, 0.5*inch))

# # Добавляем заголовок для второй таблицы
# story.append(Paragraph("Таблица 2", styles['Heading1']))
# story.append(Spacer(1, 0.25*inch))
# story.append(table2)

# # Добавляем дополнительные таблицы (по аналогии)
# # story.append(Paragraph("Таблица 3", styles['Heading1']))
# # story.append(Spacer(1, 0.25*inch))
# # story.append(table3)

# # Собираем документ
# doc.build(story)

# print("Отчёт успешно создан: tables_report.pdf")
# ========== код 4
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import landscape, A4
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch

# # Настройки страницы
# PAGE_WIDTH, PAGE_HEIGHT = landscape(A4) # Альбомная ориентация A4
# margin = 0.5 * inch

# # Создаём документ
# pdf_path = "two_tables_side_by_side.pdf"
# doc = SimpleDocTemplate(pdf_path, pagesize=landscape(A4),
# leftMargin=margin, rightMargin=margin,
# topMargin=margin, bottomMargin=margin)

# # Стили
# styles = getSampleStyleSheet()
# title_style = ParagraphStyle(
#     'CustomTitle',
#     parent=styles['Heading1'],
#     fontSize=14,
#     alignment=1, # 0=left, 1=center, 2=right
#     spaceAfter=10
#     )

# # Пример данных для таблиц
# data1 = [
#     ['Имя', 'Возраст'],
#     ['Анна', '25'],
#     ['Борис', '30'],
#     ['Вера', '22']
# ]

# data2 = [
#     ['Город', 'Население (тыс.)'],
#     ['Москва', '12600'],
#     ['СПб', '5400'],
#     ['Новосибирск', '1600']
#     ]

# # Создание таблиц
# table1 = Table(data1, colWidths=[1.5*inch, 1*inch])
# table2 = Table(data2, colWidths=[1.8*inch, 1.2*inch])

# # Стилизация таблиц
# for table in (table1, table2):
#     table.setStyle(TableStyle([
#     ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
#     ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#     ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     ]))

# # Функция для компоновки двух таблиц в строку
# def make_row_of_tables(title1, table1, title2, table2):
#     from reportlab.platypus import Table as PlatypusTable

#     # Формируем "столбцы" для размещения таблиц в ряд
#     # Каждая "ячейка" содержит заголовок и таблицу вертикально
#     col1 = [Paragraph(title1, title_style), table1]
#     col2 = [Paragraph(title2, title_style), table2]

#     # Создаём внешнюю таблицу 1x2
#     combined = PlatypusTable([[col1, col2]],colWidths=[(PAGE_WIDTH - 2 * margin) / 2 - 0.2*inch] * 2,
#     hAlign='CENTER')
#     combined.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
#                                     ('LEFTPADDING', (0, 0), (-1, -1), 10),
#                                     ('RIGHTPADDING', (0, 0), (-1, -1), 10),
#                                     ]))
#     return combined

# # Сборка документа
# elements = []

# # Добавляем объединённую структуру
# elements.append(make_row_of_tables("Таблица 1: Люди", table1, "Таблица 2: Города", table2))

# # Формируем PDF
# doc.build(elements)

# print(f"PDF успешно создан: {pdf_path}")
# from reportlab.lib.pagesizes import A4, landscape
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.lib.units import cm
# import os

# def create_tables_document():
# # Создаем PDF документ с альбомной ориентацией
#     filename = "tables_document.pdf"
#     doc = SimpleDocTemplate(filename, pagesize=landscape(A4),
#                             topMargin=1*cm, bottomMargin=1*cm,
#                             leftMargin=1*cm, rightMargin=1*cm)

#         # Стили для заголовков и таблиц
#     styles = getSampleStyleSheet()
#     title_style = ParagraphStyle(
#     'CustomTitle',
#     parent=styles['Heading2'],
#     fontSize=12,
#     spaceAfter=12,
#     alignment=1 # Выравнивание по центру
#     )

#     elements = []

#     # Данные для таблиц (пример)
#     table_data = [
#         [['Заголовок 1', 'Заголовок 2'], ['Данные 1', 'Данные 2']],
#         [['Пункт A', 'Пункт B'], ['Значение 1', 'Значение 2']],
#         [['Имя', 'Возраст'], ['Анна', '25']],
#         [['Город', 'Население'], ['Москва', '12 млн']],
#         [['Продукт', 'Цена'], ['Телефон', '500$']],
#         [['Дата', 'Событие'], ['01.01.2024', 'Конференция']],
#         [['Проект', 'Статус'], ['Разработка', 'В процессе']],
#         [['Отдел', 'Бюджет'], ['IT', '100000$']]
#         ]

#     # Создаем 8 таблиц с заголовками
#     tables = []
#     for i, data in enumerate(table_data, 1):
#     # Создаем заголовок для таблицы
#         title = Paragraph(f"Таблица {i}: {data[0][0]} - {data[0][1]}", title_style)

#     # Создаем таблицу
#     table = Table(data, colWidths=[4*cm, 4*cm])

#     # Стилизуем таблицу
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, 0), 10),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black)
#         ]))

#     tables.append((title, table))

#     # Размещаем таблицы по 2 в ряд в 4 ряда
#     for row in range(4):
#         row_tables = tables[row*2:row*2+2]

#     # Создаем контейнер для двух таблиц в строке
#     row_data = []
#     for title, table in row_tables:
#         row_data.extend([title, table])

#     # Создаем таблицу для размещения двух таблиц в одной строке
#     if len(row_tables) == 2:
#         two_tables_table = Table([[row_data[0], row_data[2]],
#         [row_data[1], row_data[3]]],
#         colWidths=[8*cm, 8*cm])

#         two_tables_table.setStyle(TableStyle([
#             ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#             ('LEFTPADDING', (0, 0), (-1, -1), 10),
#             ('RIGHTPADDING', (0, 0), (-1, -1), 10),
#             ]))

#         elements.append(two_tables_table)
#         elements.append(Spacer(1, 0.5*cm))

#         # Создаем документ
#         doc.build(elements)
#         print(f"Документ создан: {filename}")
#         return filename

# # # Альтернативный вариант с использованием более простого подхода
# # def create_tables_document_simple():
# # filename = "tables_document_simple.pdf"
# # doc = SimpleDocTemplate(filename, pagesize=landscape(A4),
# # topMargin=1*cm, bottomMargin=1*cm,
# # leftMargin=1*cm, rightMargin=1*cm)

# # styles = getSampleStyleSheet()
# # title_style = ParagraphStyle(
# # 'CustomTitle',
# # parent=styles['Heading3'],
# # fontSize=10,
# # spaceAfter=6,
# # alignment=1
# # )

# # elements = []

# # # Создаем данные для всех таблиц
# # all_tables_data = []
# # for i in range(1, 9):
# # title = Paragraph(f"Таблица {i}", title_style)

# # # Пример данных таблицы
# # table_data = [
# # [f'Колонка 1', f'Колонка 2', f'Колонка 3'],
# # [f'Данные {i}.1', f'Данные {i}.2', f'Данные {i}.3'],
# # [f'Данные {i}.4', f'Данные {i}.5', f'Данные {i}.6']
# # ]

# # table = Table(table_data, colWidths=[3*cm, 3*cm, 3*cm])
# # table.setStyle(TableStyle([
# # ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F81BD')),
# # ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
# # ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
# # ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
# # ('FONTSIZE', (0, 0), (-1, 0), 8),
# # ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#DCE6F1')),
# # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
# # ('FONTSIZE', (0, 1), (-1, -1), 8),
# # ]))

# # all_tables_data.append((title, table))

# # # Размещаем таблицы по 2 в ряд
# # for i in range(0, 8, 2):
# # if i + 1 < len(all_tables_data):
# # # Создаем строку с двумя таблицами
# # row_table = Table([
# # [all_tables_data[i][0], all_tables_data[i+1][0]],
# # [all_tables_data[i][1], all_tables_data[i+1][1]]
# # ], colWidths=[9*cm, 9*cm])

# # row_table.setStyle(TableStyle([
# # ('VALIGN', (0, 0), (-1, -1), 'TOP'),
# # ('LEFTPADDING', (0, 0), (-1, -1), 5),
# # ('RIGHTPADDING', (0, 0), (-1, -1), 5),
# # ]))

# # elements.append(row_table)
# # elements.append(Spacer(1, 0.3*cm))

# # doc.build(elements)
# # print(f"Документ создан: {filename}")
# # return filename

# if __name__ == "__main__":
# # Создаем документы
#     create_tables_document()
# # create_tables_document_simple()
# # Отправлено с iPhone

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
import os

def create_tables_document():
# Создаем PDF документ с альбомной ориентацией
    filename = "tables_document.pdf"
    doc = SimpleDocTemplate(filename, pagesize=landscape(A4),
    topMargin=1*cm, bottomMargin=1*cm,
    leftMargin=1*cm, rightMargin=1*cm)

# Стили для заголовков и таблиц
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
'CustomTitle',
parent=styles['Heading2'],
fontSize=12,
spaceAfter=12,
alignment=1 # Выравнивание по центру
)

elements = []

# Данные для таблиц (пример)
table_data = [
[['Заголовок 1', 'Заголовок 2'], ['Данные 1', 'Данные 2']],
[['Пункт A', 'Пункт B'], ['Значение 1', 'Значение 2']],
[['Имя', 'Возраст'], ['Анна', '25']],
[['Город', 'Население'], ['Москва', '12 млн']],
[['Продукт', 'Цена'], ['Телефон', '500$']],
[['Дата', 'Событие'], ['01.01.2024', 'Конференция']],
[['Проект', 'Статус'], ['Разработка', 'В процессе']],
[['Отдел', 'Бюджет'], ['IT', '100000$']]
]

# Создаем 8 таблиц с заголовками
tables = []
for i, data in enumerate(table_data, 1):
# Создаем заголовок для таблицы
    title = Paragraph(f"Таблица {i}: {data[0][0]} - {data[0][1]}", title_style)

    # Создаем таблицу
    table = Table(data, colWidths=[4*cm, 4*cm])

# Стилизуем таблицу
table.setStyle(TableStyle([
('BACKGROUND', (0, 0), (-1, 0), colors.grey),
('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
('ALIGN', (0, 0), (-1, -1), 'CENTER'),
('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
('FONTSIZE', (0, 0), (-1, 0), 10),
('BOTTOMPADDING', (0, 0), (-1, 0), 12),
('BACKGROUND', (0, 1), (-1, -1), colors.beige),
('GRID', (0, 0), (-1, -1), 1, colors.black)
]))

tables.append((title, table))

# Размещаем таблицы по 2 в ряд в 4 ряда
for row in range(4):
    row_tables = tables[row*2:row*2+2]

# Создаем контейнер для двух таблиц в строке
row_data = []
for title, table in row_tables:
    row_data.extend([title, table])

# Создаем таблицу для размещения двух таблиц в одной строке
if len(row_tables) == 2:
    two_tables_table = Table([[row_data[0], row_data[2]],
    [row_data[1], row_data[3]]],
    colWidths=[8*cm, 8*cm])

    two_tables_table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))

    elements.append(two_tables_table)
    elements.append(Spacer(1, 0.5*cm))

#     # Создаем документ
#     doc.build(elements)
#     print(f"Документ создан: {filename}")
#     return filename

# # Альтернативный вариант с использованием более простого подхода
# def create_tables_document_simple():
#     filename = "tables_document_simple.pdf"
#     doc = SimpleDocTemplate(filename, pagesize=landscape(A4),
#     topMargin=1*cm, bottomMargin=1*cm,
#     leftMargin=1*cm, rightMargin=1*cm)

# styles = getSampleStyleSheet()
# title_style = ParagraphStyle(
# 'CustomTitle',
# parent=styles['Heading3'],
# fontSize=10,
# spaceAfter=6,
# alignment=1
# )

# elements = []

# # Создаем данные для всех таблиц
# all_tables_data = []
# for i in range(1, 9):
# title = Paragraph(f"Таблица {i}", title_style)

# # Пример данных таблицы
# table_data = [
# [f'Колонка 1', f'Колонка 2', f'Колонка 3'],
# [f'Данные {i}.1', f'Данные {i}.2', f'Данные {i}.3'],
# [f'Данные {i}.4', f'Данные {i}.5', f'Данные {i}.6']
# ]

# table = Table(table_data, colWidths=[3*cm, 3*cm, 3*cm])
# table.setStyle(TableStyle([
# ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F81BD')),
# ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
# ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
# ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
# ('FONTSIZE', (0, 0), (-1, 0), 8),
# ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#DCE6F1')),
# ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
# ('FONTSIZE', (0, 1), (-1, -1), 8),
# ]))

# all_tables_data.append((title, table))

# # Размещаем таблицы по 2 в ряд
# for i in range(0, 8, 2):
# if i + 1 < len(all_tables_data):
# # Создаем строку с двумя таблицами
# row_table = Table([
# [all_tables_data[i][0], all_tables_data[i+1][0]],
# [all_tables_data[i][1], all_tables_data[i+1][1]]
# ], colWidths=[9*cm, 9*cm])

# row_table.setStyle(TableStyle([
# ('VALIGN', (0, 0), (-1, -1), 'TOP'),
# ('LEFTPADDING', (0, 0), (-1, -1), 5),
# ('RIGHTPADDING', (0, 0), (-1, -1), 5),
# ]))

# elements.append(row_table)
# elements.append(Spacer(1, 0.3*cm))

# doc.build(elements)
# print(f"Документ создан: {filename}")
# return filename

# if __name__ == "__main__":
# # Создаем документы
#     create_tables_document()
#     create_tables_document_simple()
