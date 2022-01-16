from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.views.generic import View

from repairs.models import Repair
from utils.html_to_pdf import render_to_pdf


class GeneratePdf(View):
    def get(self, request, repair_id):
        repair = get_object_or_404(Repair, id=repair_id)
        context = {
            'repair': repair,
        }
        template = get_template('repairs/sheet.html')
        html = template.render(context)
        pdf = render_to_pdf(html)
        return HttpResponse(pdf.getvalue(), content_type='application/pdf')
