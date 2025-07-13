from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import InternalMarks, Student, Result, CLASS_SUBJECTS
from rest_framework import viewsets
from .serializers import StudentSerializer, ResultSerializer



def index(request):
    return render(request, 'index.html')


def login_view(request):
    error = None
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            error = 'Invalid username or password.'
    return render(request, 'login.html', {'error': error})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def register_student(request):
    class_range = range(1, 11) 
    if request.method == 'POST':
        data = request.POST
        Student.objects.create(
            name=data['name'],
            father_name=data['father_name'],
            mother_name=data['mother_name'],
            roll_number=data['roll_number'],
            class_name=data['class_name'],
            address=data['address']
        )
        return redirect('list_students')
    return render(request, 'register.html', {'class_range': class_range})


@login_required
def list_students(request):
    students = Student.objects.all()
    return render(request, 'list.html', {'students': students})


@login_required
def edit_student(request, student_id):
    class_range = range(1, 11)
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.name = request.POST['name']
        student.father_name = request.POST['father_name']
        student.mother_name = request.POST['mother_name']
        student.roll_number = request.POST['roll_number']
        student.class_name = request.POST['class_name']
        student.address = request.POST['address']
        student.save()
        return redirect('list_students')
    return render(request, 'edit_student.html', {'student': student, 'class_range': class_range})


@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('list_students')


@login_required
def view_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'student_profile.html', {'student': student})



@login_required
def upload_result(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    subjects = CLASS_SUBJECTS.get(student.class_name, [])
    exam_types = ['PT-1', 'PT-2', 'SA-1', 'TERM-1']

    if request.method == 'POST':
        exam_type = request.POST.get('exam_type')

        if exam_type == "TERM-1":
            for subject in subjects:
                InternalMarks.objects.update_or_create(
                    student=student,
                    subject=subject,
                    exam_type='TERM-1',
                    defaults={
                        'attendance': int(request.POST.get(f'attendance_{subject}', 0)),
                        'notebook': int(request.POST.get(f'notebook_{subject}', 0)),
                        'discipline': 0  # or remove if unused
                    }
                )
        else:
            # ✅ Save PT-1, PT-2, SA-1
            for subject in subjects:
                marks = request.POST.get(subject)
                if marks:
                    if exam_type == 'SA-1':
                        full_marks = 80
                        passing_marks = 33
                    else:
                        full_marks = 50
                        passing_marks = 20

                    Result.objects.update_or_create(
                        student=student,
                        subject=subject,
                        exam_type=exam_type,
                        defaults={
                            'marks_obtained': float(marks),
                            'full_marks': full_marks,
                            'passing_marks': passing_marks
                        }
                    )

        return redirect('view_student', student_id=student_id)

    return render(request, 'upload_result.html', {
        'student': student,
        'subjects': subjects,
        'exam_types': exam_types
    })



@login_required
def show_result(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    exam_type = request.GET.get('exam_type', 'PT-1')
    subjects = CLASS_SUBJECTS.get(student.class_name, [])
    results_data = []
    total_obtained = 0

    def calculate_grade(percentage):
        if percentage >= 90:
            return "A+"
        elif percentage >= 75:
            return "A"
        elif percentage >= 60:
            return "B"
        elif percentage >= 45:
            return "C"
        elif percentage >= 33:
            return "D"
        else:
            return "F"

    # 
    if exam_type == 'TERM-1':
     for subject in subjects:
        pt1 = Result.objects.filter(student=student, subject=subject, exam_type='PT-1').first()
        pt2 = Result.objects.filter(student=student, subject=subject, exam_type='PT-2').first()
        sa1 = Result.objects.filter(student=student, subject=subject, exam_type='SA-1').first()
        internals = InternalMarks.objects.filter(student=student, subject=subject, exam_type='TERM-1').first()

        pt1_marks = pt1.marks_obtained if pt1 else 0
        pt2_marks = pt2.marks_obtained if pt2 else 0
        sa1_marks = sa1.marks_obtained if sa1 else 0
        attendance = internals.attendance if internals else 0
        notebook = internals.notebook if internals else 0

        pt_avg_raw = (pt1_marks + pt2_marks) / 2 if pt1 or pt2 else 0
        pt_avg_scaled = (pt_avg_raw / 50) * 10

        final_marks = pt_avg_scaled + sa1_marks
        internal_total = attendance + notebook
        subject_total = final_marks + internal_total
        subject_percentage = (subject_total / 100) * 100 if subject_total else 0
        grade = calculate_grade(subject_percentage)

        results_data.append({
            'subject': subject,
            'pt1_marks': round(pt1_marks, 2),
            'pt2_marks': round(pt2_marks, 2),
            'pt_avg_scaled': round(pt_avg_scaled, 2),
            'sa1_marks': round(sa1_marks, 2),
            'final_marks': round(final_marks, 2),
            'attendance': round(attendance, 2),
            'notebook': round(notebook, 2),
            'internal_total': round(internal_total, 2),
            'subject_total': round(subject_total, 2),
            'grade': grade,
        })

        total_obtained += subject_total

        total_full = len(subjects) * 100
        percentage = (total_obtained / total_full) * 100 if total_full else 0

        context = {
           'student': student,
         'term1_results': results_data,
         'marks_obtained': round(total_obtained, 2),
         'total_full': total_full,
         'percentage': round(percentage, 2),
         'exam_types': ['PT-1', 'PT-2', 'SA-1', 'TERM-1'],
         'exam_type': exam_type,
        }
        print(results_data)
     return render(request, 'term1_result.html', context)

    
    else:
        print(subjects)
        for subject in subjects:
            result = Result.objects.filter(student=student, subject=subject, exam_type=exam_type).first()
            marks = result.marks_obtained if result else 0
            grade = result.get_grade() if result else "-"
            results_data.append({
                'subject': subject,
                'marks': round(marks, 2),
                'full_marks': result.full_marks if result else 0,
                'passing_marks': result.passing_marks if result else 0,
                'grade': grade
            })
            total_obtained += marks
    
        total_full = sum(r['full_marks'] for r in results_data)
        percentage = (total_obtained / total_full) * 100 if total_full else 0
    
        context = {
            'student': student,
            'results': results_data,
            'marks_obtained': round(total_obtained, 2),
            'total_full': total_full,
            'percentage': round(percentage, 2),
            'exam_types': ['PT-1', 'PT-2', 'SA-1', 'TERM-1'],
            'exam_type': exam_type,
        }
        return render(request, 'show_result.html', context)
    


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer