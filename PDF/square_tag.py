import os
import sys
import pdfrw
import logging
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
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start(color_type, color_name, color_price, tea_type, name_of_tea, price_tea):
    try:
        #START
        template_path = 'PDF/template/square_tag.pdf'
        output_file = f'PDF/output_PDF/square/{name_of_tea}.pdf'
        locale = 'PDF/fonts/Capsmall_clean.ttf'
        pdfmetrics.registerFont(TTFont('Capsmall_clean', locale))

        page_width = 6.79 * cm
        page_height = 6.73 * cm

        template = PdfReader(template_path)
        page = template.pages[0]

        page_xobj = pagexobj(page)

        c = canvas.Canvas(output_file, pagesize=(page_width, page_height))

        c.doForm(makerl(c, page_xobj))
        with edit_canvas(output_file, page_width, page_height) as c:
            c.doForm(makerl(c, page_xobj))
            type_tea(c, color_type, tea_type.upper(), 27)
            name_tea(c, color_name, 14, str(name_of_tea).upper().replace('/', '\\'))
            price_of_tea(c, color_price, price_tea,  19)
        trim_bottom = 2.9 * mm  # 10 мм снизу
        resize_page(output_file, page_width, page_height, trim_bottom)
    except Exception as e:
        logger.error(e)


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
        logger.error(e)


def draw_background(c, x, y, width, height, background_color):
    try:
        c.setFillColor(background_color)
        c.rect(x, y, width, height, fill=True)
    except Exception as e:
        logger.error(e)


def get_name_tea_style(font_name='Capsmall_clean', font_size=15, font_color=colors.white):
    try:
        return ParagraphStyle(
            name='NameTea',
            fontName=font_name,
            fontSize=font_size,
            textColor=font_color,
            alignment=TA_CENTER,
            leading=0.9 * font_size,  # уменьшение разрыва между строками
        )
    except Exception as e:
        logger.error(e)


def name_tea(c, color_id, size, name_of_tea):
    try:

        pdf_color = colors.HexColor(color_id)
        c.setFillColor(pdf_color)
        width = 4 * cm
        height = 1 * cm
        x = 1.55 * cm
        y = 2.48 * cm
        # draw_background(c, x, y, width, height, background_color=colors.HexColor('#CCCCCC'))

        # Уменьшение размера шрифта в зависимости от длины текста
        if len(name_of_tea) >= 40:
            size -= 5.7
        elif len(name_of_tea) >= 31:
            size -= 4
        elif len(name_of_tea) >= 25:
            size -= 4
        elif len(name_of_tea) > 20:
            size -= 3
        elif len(name_of_tea) > 15:
            size -= 2
        elif len(name_of_tea) > 10:
            size -= 1
        elif len(name_of_tea) <= 6:
            size += 8
        elif len(name_of_tea) <= 4:
            size += 4

        # Подсветка зон размещения
        # draw_background(c, x, y, width, height, background_color=colors.HexColor('#CCCCCC'))  # добавьте эту строку

        name_tea_style = get_name_tea_style(font_size=size, font_color=pdf_color)
        name_tea_paragraph = Paragraph(name_of_tea, style=name_tea_style)
        wrapped_text_width, wrapped_text_height = name_tea_paragraph.wrap(width, height)

        # Вычисление вертикального отступа для центрирования текста
        vertical_padding = (height - wrapped_text_height) / 2
        name_tea_paragraph.drawOn(c, x, y + vertical_padding)
    except Exception as e:
        logger.error(e)


def type_tea(c, color_id, tea_type, size):
    try:
        x = 1.85 * cm
        y = 3.5 * cm
        width = 3.3 * cm
        height = 1.5 * cm
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
        logger.error(e)


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
        x = 1.95 * cm
        y = 1.7 * cm
        width = 3.1 * cm
        height = 0.9 * cm

        if len(price_tea) >= 10:
            size -= 3
        elif len(price_tea) >= 11:
            size -= 4

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
        logger.error(e)


@contextmanager
def edit_canvas(output_file, page_width, page_height):
    c = canvas.Canvas(output_file, pagesize=(page_width, page_height))
    try:
        yield c
    finally:
        c.save()


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
        logger.error(e)