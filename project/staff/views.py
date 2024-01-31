from django.shortcuts import render

from staff.models import Dept


def dept_select_view(request):
    context = {'dept_list': Dept.objects.all()}
    return render(request, 'staff/dept_select.html', context)
