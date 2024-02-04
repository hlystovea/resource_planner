from django.urls import path

from staff import views


app_name = 'staff'

urlpatterns = [
    path('dept/select/', views.dept_select_view, name='dept-select'),
]
