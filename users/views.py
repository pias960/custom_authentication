from django.shortcuts import render
from account.decorators import is_user
# Create your views here.
@is_user('admin')
def admin_dashboard(request):
    return render(request, 'users/admin_dashboard.html')
@is_user('student')
def student_dashboard(request):
    return render(request, 'users/student_dashboard.html')
@is_user('teacher')
def teacher_dashboard(request):
    return render(request, 'users/teacher_dashboard.html')
