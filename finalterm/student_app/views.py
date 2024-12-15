from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Subject, Score


def student_detail(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    scores = Score.objects.filter(student=student)
    total_score = sum(score.score for score in scores)
    avg_score = round(total_score / scores.count(), 2) if scores else 0
    grade = 'A' if avg_score >= 80 else 'B' if avg_score >= 60 else 'C'
    return render(request, 'student_app/student_detail.html', {
        'student': student,
        'scores': scores,
        'avg_score': avg_score,
        'grade': grade
    })

def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    scores = Score.objects.filter(subject=subject)
    students = Student.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student')
        score_value = request.POST.get('score')
        student = get_object_or_404(Student, id=student_id)
        Score.objects.create(student=student, subject=subject, score=score_value)
        return redirect('subject_detail', subject_id=subject.id)

    return render(request, 'student_app/subject_detail.html', {
        'subject': subject,
        'scores': scores,
        'students': students
    })

def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        subject.delete()
        return redirect('main_page')

    return render(request, 'student_app/confirm_delete.html', {'subject': subject})

def add_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        # 새로운 과목을 추가하는 코드
        Subject.objects.create(name=name, description=description)
        return redirect('main_page')  # 과목 추가 후 첫 페이지로 리디렉션
    return render(request, 'student_app/add_subject.html')  # 과목 추가 폼을 보여주는 템플릿


def main_page(request):
    # 학생 정보와 과목 정보를 가져옵니다.
    students = Student.objects.all()
    subjects = Subject.objects.all()

    student_data = []
    
    # 학생별로 평균 점수와 grade를 계산합니다.
    for student in students:
        scores = student.scores.all()  # 학생의 성적을 가져옵니다.
        total_score = sum(score.score for score in scores) if scores else 0
        avg_score = round(total_score / len(scores), 2) if scores else 0
        grade = 'A' if avg_score >= 80 else 'B' if avg_score >= 60 else 'C'

        # 학생 정보를 딕셔너리로 저장합니다.
        student_data.append({
            'id': student.student_id,
            'name': student.name,
            'age': student.age,
            'avg_score': avg_score,
            'grade': grade
        })

    # 템플릿에 데이터 전달
    return render(request, 'student_app/home.html', {
        'students': student_data,
        'subjects': subjects
    })
