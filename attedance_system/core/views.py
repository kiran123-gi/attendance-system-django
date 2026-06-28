from django.shortcuts import render
from .models import Student, Attendance
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd

# Home
def home(request):
    students = Student.objects.all()
    return render(request, 'core/home.html', {'students': students})


# Add student
@csrf_exempt
def add_student(request):
    if request.method == "POST":
        name = request.POST.get('name')
        Student.objects.create(name=name)
        return JsonResponse({'message': 'added'})
    return JsonResponse({'error': 'invalid'}, status=400)


# Mark attendance
@csrf_exempt
def mark_attendance(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        status = request.POST.get('status') == 'true'

        student = Student.objects.get(id=student_id)
        Attendance.objects.create(student=student, status=status)

        return JsonResponse({'message': 'ok'})
    return JsonResponse({'error': 'invalid'}, status=400)


# Dashboard
def dashboard_data(request):
    students = Student.objects.all()
    data = []

    for s in students:
        total = Attendance.objects.filter(student=s).count()
        present = Attendance.objects.filter(student=s, status=True).count()
        absent = total - present

        percent = (present / total * 100) if total > 0 else 0

        data.append({
            'name': s.name,
            'present': present,
            'absent': absent,
            'percentage': round(percent, 2)
        })

    return JsonResponse({'data': data})


# Excel upload
@csrf_exempt
def upload_excel(request):
    if request.method == "POST":
        file = request.FILES['file']

        df = pd.read_excel(file)

        for _, row in df.iterrows():
            student, _ = Student.objects.get_or_create(name=row['name'])

            Attendance.objects.create(
                student=student,
                date=row['date'],  # date column from excel
                status=True if row['status'] == "Present" else False
            )

        return JsonResponse({'message': 'Excel uploaded successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)