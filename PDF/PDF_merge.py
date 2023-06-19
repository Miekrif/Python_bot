import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


import os
import pdfrw
from reportlab.pdfgen import canvas
from pdfrw import PdfReader, PdfWriter, PageMerge


def create_a4_pdf(tea_list, output_file):
    a4_width, a4_height = 595.44, 841.68
    tea_width, tea_height = 6.73, 6.79
    max_x, max_y = a4_width, a4_height
    x_pos, y_pos = 0, 0
    pdf_writer = PdfWriter()

    pdf_page = None

    for tea_filename in tea_list:
        if x_pos + tea_width > max_x:
            x_pos = 0
            y_pos += tea_height

        if not pdf_page or y_pos + tea_height > max_y:
            c = canvas.Canvas('blank_page.pdf', pagesize=(a4_width, a4_height))
            c.showPage()
            c.save()
            pdf_page = pdfrw.PdfReader('blank_page.pdf').pages[0]
            x_pos, y_pos = 0, 0

        tea_page_pdf = pdfrw.PdfReader('output/6.79_6.73/' + tea_filename)
        tea_page_obj = tea_page_pdf.pages[0]

        # Изменение положения объекта PDF
        tea_page_obj.MediaBox = [x_pos, y_pos, x_pos + tea_width, y_pos + tea_height]

        PageMerge(pdf_page).add(tea_page_obj)

        x_pos += tea_width

        if y_pos + tea_height > max_y:
            pdf_writer.addpage(pdf_page)
            pdf_page = None

    if pdf_page:
        pdf_writer.addpage(pdf_page)
    import io

    with io.open(output_file, 'wb') as output:
        pdf_data = pdfrw.PdfWriter().write(pdf_writer)
        output.write(pdf_data.encode('utf-8', 'ignore'))

    # with open(output_file, "wb") as output:
    #     pdf_data = pdfrw.PdfWriter().write(pdf_writer)
    #     output.write(pdf_data.encode('utf-8', 'ignore'))
    #
    #     output.write(pdfrw.PdfWriter().write(pdf_writer))
