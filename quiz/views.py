from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from .models import Question, Quiz
# Create your views here.


def quiz(request, quizID):
    try:
        quiz = get_object_or_404(Quiz, id=quizID)
        print(request.user.id)
        print(quiz.teacher_id)
        print(quiz.classes)
        print(quiz.level)
    except:
        print('whoops 3')
        return redirect('index')

    if request.user.is_authenticated:
        try:
            if (request.user.classes == quiz.classes) & (request.user.level == quiz.level) & (request.user.teacher == quiz.teacher_id):
                print('whoops 1')
                questionList = get_list_or_404(Question, quiz=quizID)

                context = {
                    'questions': questionList
                }
        except:
            if (request.user.id == quiz.teacher_id):
                print('whoops 2')
                questionList = get_list_or_404(Question, quiz=quizID)
                print(questionList[0].correct_answer_value)
                context = {
                    'questions': questionList
                }
                return render(request, 'quiz/quiz.html', context)
    else:
        return redirect('index')
