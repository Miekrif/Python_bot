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
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def start(color_type, color_name, color_price, tea_type, name_of_tea, price_tea):
    #START
    template_path = 'template/horizon_tag.pdf'
    output_file = f'output/horizon/{name_of_tea}.pdf'

    locale = 'fonts/Capsmall_clean.ttf'
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


def split_text(text, max_length):
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


def draw_background(c, x, y, width, height, background_color):
    c.setFillColor(background_color)
    c.rect(x, y, width, height, fill=True)


def get_name_tea_style(font_name='Capsmall_clean', font_size=15, font_color=colors.white):
    return ParagraphStyle(
        name='NameTea',
        fontName=font_name,
        fontSize=font_size,
        textColor=font_color,
        alignment=TA_CENTER,
        leading=0.9 * font_size,  # уменьшение разрыва между строками
    )

def name_tea(c, color_id, size, name_of_tea):
    pdf_color = colors.HexColor(color_id)
    c.setFillColor(pdf_color)
    width = 18.5 * cm
    height = 1.9 * cm
    x = 3 * cm
    y = 1 * cm
    # draw_background(c, x, y, width, height, background_color=colors.HexColor('#CCCCCC'))

    # Уменьшение размера шрифта в зависимости от длины текста
    if len(name_of_tea) > 30:
        size -= 6
    elif len(name_of_tea) > 20:
        size -= 3
    elif len(name_of_tea) > 15:
        size -= 2
    elif len(name_of_tea) > 10:
        size -= 1

    name_tea_style = get_name_tea_style(font_size=size, font_color=pdf_color)
    name_tea_paragraph = Paragraph(name_of_tea, style=name_tea_style)
    wrapped_text_width, wrapped_text_height = name_tea_paragraph.wrap(width, height)

    # Вычисление вертикального отступа для центрирования текста
    vertical_padding = (height - wrapped_text_height) / 2
    name_tea_paragraph.drawOn(c, x, y + vertical_padding)


def type_tea(c, color_id, tea_type, size):
    x = 4.9 * cm
    y = 1.4 * cm
    c.setFont('Capsmall_clean', size)

    pdf_color = colors.HexColor(color_id)

    c.setFillColor(pdf_color)
    c.drawCentredString(x, y, tea_type)


def price_of_tea(c, color_id, price_tea, size):
    x = 18.5 * cm
    y = 1.5 * cm

    c.setFont('Capsmall_clean', size)

    pdf_color = colors.HexColor(color_id)

    c.setFillColor(pdf_color)

    c.drawCentredString(x, y, price_tea)


@contextmanager
def edit_canvas(output_file, page_width, page_height):
    c = canvas.Canvas(output_file, pagesize=(page_width, page_height))
    try:
        yield c
    finally:
        c.save()


def resize_page(output_file, page_width, page_height, trim_bottom):
    # Чтение исходного PDF-файла
    input_pdf = pdfrw.PdfReader(output_file)

    # Обновление размеров страницы
    new_page_height = page_height - trim_bottom
    for page in input_pdf.pages:
        page.MediaBox = [0, trim_bottom, page_width, page_height]

    # Сохранение обновленного PDF-файла
    pdfrw.PdfWriter().write(output_file, input_pdf)