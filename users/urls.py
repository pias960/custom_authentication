from django.urls import path
from .views import *

urlpatterns = [
    path('admin_dash/', admin_dashboard, name='admin_dash'),
    path('student_dash/', student_dashboard, name='student_dash'),
    path('teacher_dash/', teacher_dashboard, name='teacher_dash'),
    
]
