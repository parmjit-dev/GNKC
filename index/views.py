from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404

from homework.forms import HomeworkForm
from homework.models import Homework
from students.models import Students
from teachers.models import Teacher
from quiz.models import Quiz, Question
from .emailForm import emailForm
from .enrolmentForm import enrolmentForm


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index/index.html')


def about(request):
    return render(request, 'index/about.html')


def philosophy(request):
    return render(request, 'index/philosophy.html')


def teachings(request):
    return render(request, 'index/teachings.html')


def enrolment(request):
    if request.method == 'POST':
        form = enrolmentForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['termsRead'] == '1':
                messages.success(request, 'Form sent')
                subject = form.cleaned_data['name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']
                try:
                    send_mail(subject, (email + message), 'mythosAPI@gmail.com',
                              ['parmjit.singh.1199@gmail.com'], fail_silently=True)
                    messages.success(request, 'Email sent')
                    return redirect('index')
                except:
                    form = enrolmentForm()
                    messages.error(
                        request, 'Error sending form, please email admin')
            else:
                form = enrolmentForm()
                messages.error(
                    request, 'Error sending form, please email admin')

    else:
        form = enrolmentForm()
    return render(request, 'index/enrolment.html', {'form': form})


def media(request):
    return render(request, 'index/media.html')


def parental(request):
    if request.method == 'POST':
        form = emailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, (f"from {email} \n {message}"), 'mythosAPI@gmail.com', [
                        'parmjit.singh.1199@gmail.com'], fail_silently=False)
                messages.success(request, 'Email Sent')
                return redirect('index')
            except:
                form = emailForm()
                messages.error(
                    request, 'Error sending form, please email admin')
    else:
        form = emailForm()
    return render(request, 'index/parental.html', {'form': form})


def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            print(request.user.id)
            teacher_id = get_object_or_404(Teacher, user=request.user.id)
            homework = Homework.objects.select_related(
                'teacher').filter(teacher=teacher_id)
            context = {
                'homework': homework
            }
            return render(request, 'dashboard/dashboard.html', context)
        else:
            student = get_object_or_404(Students, user_id=request.user.id)
            # homework_queryset = Homework.objects.select_related('teacher').filter(
            # teacher=student.teacher)

            homework = get_list_or_404(
                Homework, classes=student.classes, level=student.level, teacher=student.teacher)

            context = {
                'homework': homework
            }
            return render(request, 'dashboard/dashboard.html', context)
    messages.error(
        request, 'You are not authenticated')
    return redirect('index')


def homework(request):
    if request.user.is_authenticated & request.user.is_staff:
        if request.method == 'POST':
            print(request.user.pk)
            teacher_id = Teacher.objects.select_related(
                'user').get(user_id=request.user.pk)
            print(request.POST)
            form = HomeworkForm(request.POST)
            if form.is_valid():
                print(request.user.id)
                new_form = form.save(commit=False)
                new_form.teacher = teacher_id
                new_form.save()
                print('worked')
                messages.info(request, 'Homework set')
                return redirect('dashboard')
            else:
                messages.info(request, 'Error in Homework Form')
                form = HomeworkForm()
                return render(request, 'dashboard/setHomework.html', {'form': form})
        else:
            form = HomeworkForm()
            return render(request, 'dashboard/setHomework.html', {'form': form})
    messages.error(
        request, 'You are not authenticated')
    return redirect('index')


def quizzes(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            teacher_id = get_object_or_404(Teacher, user_id=request.user.id)
            quizzes = Quiz.objects.select_related(
                'teacher').filter(teacher=teacher_id)
            print(quizzes)
            quiz_Data = list(quizzes.values())
            print(quiz_Data)
            context = {
                'quizzes': quizzes,
                # 'questions': questions
            }
            return render(request, 'quiz/quizzes.html', context)
        else:
            student = get_object_or_404(Students, user_id=request.user.id)
            quiz = get_list_or_404(
                Quiz, classes=student.classes, level=student.level, teacher=student.teacher)

            context = {
                'quizzes': quiz
            }
            return render(request, 'quiz/quizzes.html', context)
    messages.error(
        request, 'You are not authenticated')
    return redirect('index')
