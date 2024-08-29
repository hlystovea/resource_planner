from django.shortcuts import render


def error_400_handler(request, exception):
    return render(request, 'errors/400.html', status=400)


def error_403_handler(request, exception):
    return render(request, 'errors/403.html', status=403)


def error_404_handler(request, exception):
    return render(request, 'errors/404.html', status=404)


def error_500_handler(request):
    return render(request, 'errors/500.html', status=500)
