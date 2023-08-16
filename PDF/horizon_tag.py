import sys
import pdfrw
from pdfrw import PdfReader
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.pagesizes import *
from contextlib import contextmanager
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def start(color_type, color_name, color_price, tea_type, name_of_tea, price_tea):
    try:
        #START
        template_path = 'PDF/template/horizon_tag.pdf'
        output_file = f'PDF/output/horizon/{name_of_tea}.pdf'

        locale = 'PDF/fonts/Capsmall_clean.ttf'
        pdfmetrics.registerFont(TTFont('Capsmall_clean', locale))

        page_width = 21 * cm
        page_height = 3.2 * cm

        template = PdfReader(template_path)
        page = template.pages[0]

        page_xobj = pagexobj(page)

        c = canvas.Canvas(output_file, pagesize=(page_width, page_height))

        c.doForm(makerl(c, page_xobj))
        with edit_canvas(output_file, page_width, page_height) as c:
            c.doForm(makerl(c, page_xobj))
            type_tea(c=c, color_id=color_type, tea_type=tea_type.upper(), size=30)
            name_tea(c=c, color_id=color_name, size=29, name_of_tea=name_of_tea.upper().replace('/', '\\'))
            price_of_tea(c=c, color_id=color_price, price_tea=price_tea,  size=25)
        trim_bottom = 2.9 * mm  # 10 мм снизу
        resize_page(output_file, page_width, page_height, trim_bottom)
    except Exception as e:
        print(e)


def split_text(text, max_length):
    try:
        if len(text) <= max_length:
            return [text]

        words = text.split(' ')
        lines = []
        current_line = ''

        for word in words:
            if len(current_line) + len(word) <= max_length:
                current_line += word + ' '
            else:
                lines.append(current_line.strip())
                current_line = word + ' '

        lines.append(current_line.strip())
        return lines
    except Exception as e:
        print(e)


def draw_background(c, x, y, width, height, background_color):
    c.setFillColor(background_color)
    c.rect(x, y, width, height, fill=True)


def get_name_tea_style(font_name='Capsmall_clean', font_size=15, font_color=colors.white):
    return ParagraphStyle(
        name='NameTea',
        fontName=font_name,
        fontSize=font_size,
        textColor=font_color,
        alignment=TA_LEFT ,  # выравнивание по левому краю
        leading=0.9 * font_size,  # уменьшение разрыва между строками
    )


def name_tea(c, color_id, size, name_of_tea):
    try:

        pdf_color = colors.HexColor(color_id)
        c.setFillColor(pdf_color)
        width = 10 * cm
        height = 1.9 * cm
        x = 8 * cm
        y = 1 * cm

        # Уменьшение размера шрифта в зависимости от длины текста
        if len(name_of_tea) > 30:
            size -= 12
        elif len(name_of_tea) > 20:
            size -= 8
        elif len(name_of_tea) > 15:
            size -= 5
        elif len(name_of_tea) > 10:
            size -= 4
        # Подсветка зон размещения
        # draw_background(c, x, y, width, height, background_color=colors.HexColor('#CCCCCC'))  # добавьте эту строку

        name_tea_style = get_name_tea_style(font_size=size, font_color=pdf_color)
        name_tea_paragraph = Paragraph(name_of_tea, style=name_tea_style)
        wrapped_text_width, wrapped_text_height = name_tea_paragraph.wrap(width, height)

        # Вычисление вертикального отступа для центрирования текста
        vertical_padding = (height - wrapped_text_height) / 2
        name_tea_paragraph.drawOn(c, x, y + vertical_padding)
    except Exception as e:
        print(e)


def type_tea(c, color_id, tea_type, size):
    try:
        x = 2.2 * cm
        y = 1 * cm
        width = 5.5 * cm
        height = 1.9 * cm
        pdf_color = colors.HexColor(color_id)

        # Подсветка зон размещения
        # draw_background(c, x, y, width, height, background_color=colors.HexColor('#CD5C5C'))

        c.setFont('Capsmall_clean', size)
        text_width = c.stringWidth(tea_type, 'Capsmall_clean', size)
        text_height = size  # Обычно размер шрифта соответствует высоте текста

        # Вычисление координат для центрирования текста
        x_centered = x + width / 2
        y_centered = y + height / 2 - text_height / 2  # Центрируем текст по вертикали внутри выделенной зоны

        c.setFillColor(pdf_color)
        c.drawCentredString(x_centered, y_centered, tea_type)
    except Exception as e:
        print(e)


def get_paragraph_style(font_name='Capsmall_clean', font_size=15, font_color=colors.white):
    return ParagraphStyle(
        name='CenteredStyle',
        fontName=font_name,
        fontSize=font_size,
        textColor=font_color,
        alignment=TA_CENTER,
        leading=0.9 * font_size  # уменьшение разрыва между строками
    )


def price_of_tea(c, color_id, price_tea, size):
    try:
        x = 18 * cm
        y = 1 * cm
        width = 2.8 * cm
        height = 1.9 * cm

        # Подсветка зон размещения
        # draw_background(c, x, y, width, height, background_color=colors.HexColor('#FFD700'))

        pdf_color = colors.HexColor(color_id)

        # Создание абзаца с заданным стилем
        style = get_paragraph_style(font_size=size, font_color=pdf_color)
        para = Paragraph(price_tea, style)

        # Размещаем абзац внутри нашей подсвеченной области
        w, h = para.wrap(width, height)
        para.drawOn(c, x, y + (height - h) / 2)

    except Exception as e:
        print(e)


@contextmanager
def edit_canvas(output_file, page_width, page_height):
    try:
        c = canvas.Canvas(output_file, pagesize=(page_width, page_height))
        try:
            yield c
        finally:
            c.save()
    except Exception as e:
        print(e)


def resize_page(output_file, page_width, page_height, trim_bottom):
    try:
        # Чтение исходного PDF-файла
        input_pdf = pdfrw.PdfReader(output_file)

        # Обновление размеров страницы
        new_page_height = page_height - trim_bottom
        for page in input_pdf.pages:
            page.MediaBox = [0, trim_bottom, page_width, page_height]

        # Сохранение обновленного PDF-файла
        pdfrw.PdfWriter().write(output_file, input_pdf)
    except Exception as e:
        print(e)