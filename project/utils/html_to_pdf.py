from io import BytesIO

from django.http import HttpResponse
from xhtml2pdf import pisa


def render_to_pdf(html: str):
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(html.encode('UTF-8')), result, encoding='UTF-8'
    )
    if pdf.err:
        return HttpResponse('Произошла ошибка <pre>' + html + '</pre>')
    return result
