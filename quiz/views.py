from django.contrib import messages
from django.contrib.messages.api import error
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from .models import Question, Quiz
from teachers.models import Teacher
from students.models import Students
from score.models import Score
from quiz.form import quizForm
from quiz.questionForm import questionForm
from django.http import HttpResponseRedirect

# def filterID(ID):
#     if(question.id == questionID):
#         del questionList[index


def quiz(request, quizID):
    if request.user.is_authenticated:
        try:
            user = get_object_or_404(Students, user_id=request.user.id)
            quiz = get_object_or_404(Quiz, pk=quizID)
        except Http404:
            return redirect('index')
        try:
            # if (user.classes == quiz.classes) & (user.level == quiz.level) & (user.teacher == quiz.teacher):
            try:
                get_object_or_404(
                    Score, first_name=request.user.first_name, last_name=request.user.last_name, quiz_id=quizID)
                messages.info(request, 'You have already done this quiz')
                return redirect('/')
            except Http404:
                questionList = get_list_or_404(Question, quiz_id=quizID)
                print(questionList)
                context = {
                    'questions': questionList,
                    'quiz': quizID,
                }
                print('worked')
                return render(request, 'quiz/quiz.html', context)
        except Http404:
            messages.error(
                request, 'You are not authenticated')
            return redirect('index')
    messages.error(
        request, 'You are not authenticated')
    return redirect('index')


def create(request):
    form = quizForm()
    addQuestionForm = questionForm()
    if request.user.is_authenticated & request.user.is_staff:
        if request.method == 'POST':
            try:
                teacher_id = get_object_or_404(
                    Teacher, user_id=request.user.pk)
                quizSubmit = quizForm(request.POST, request.FILES)
                if quizSubmit.is_valid():
                    print('valid')
                    quiz_form_submit = quizSubmit.save(commit=False)
                    quiz_form_submit.teacher_id = teacher_id.pk
                    quiz_form_submit.save()
                    quiz_id = quiz_form_submit.pk
                    messages.success(request, 'Quiz Created')
                    return render(request, 'question/question.html', {'quiz_id': quiz_id, 'form': addQuestionForm})
                return redirect('quizzes')
            except:
                messages.error(
                    request, 'error in creation - please speak to admin')
                return redirect('quizzes')
        return render(request, 'quiz/createQuiz.html', {'form': form})
    messages.error(
        request, 'You are not authenticated')
    return redirect('index')


def addQuestion(request):
    addQuestionForm = questionForm()
    if request.user.is_authenticated & request.user.is_staff:
        if request.method == 'POST':
            try:
                questionSubmit = questionForm(request.POST, request.FILES)
                quizID = request.POST['quiz_id']
                quizInstance = get_object_or_404(Quiz, pk=quizID)
                if questionSubmit.is_valid():
                    question_form_submit = questionSubmit.save(commit=False)
                    question_form_submit.quiz = quizInstance
                    question_form_submit.save()
                    try:
                        quiz_Questions = get_list_or_404(Question, quiz_id=quizID)
                        context = {
                            'questions': quiz_Questions,
                            'quiz_id': quizID,
                            'form': addQuestionForm
                        }
                    except Http404:
                        context = {
                            'quiz_id': quizID,
                            'form': addQuestionForm
                        }
                    return render(request, 'question/question.html', context)
                return render(request, 'question/question.html', {'quiz_id': quizID, 'form': addQuestionForm})
            except:
                messages.error(
                    request, 'error in creation - please speak to admin')
                return redirect('quizzes')
    messages.error(request, 'You are not authenticated')
    return redirect('quizzes')


def deleteQuestion(request, questionID):
    addQuestionForm = questionForm()
    if request.user.is_authenticated & request.user.is_staff:
        question = Question.objects.get(id=questionID)
        quizID = question.quiz_id
        question.delete()
        return render(request, 'question/question.html', {'id': quizID, 'form': addQuestionForm})
    messages.error(
        request, 'You are not authenticated')
    return redirect('index')


def deleteQuiz(request, quizID):
    if request.user.is_authenticated & request.user.is_staff:
        quiz = Quiz.objects.get(id=quizID)
        quiz.delete()
        messages.success(
            request, 'quiz deleted')
        return redirect('quizzes')
    messages.error(
        request, 'You are not authenticated')
    return redirect('index')


def updateQuiz(request, quizID):
    if request.user.is_authenticated & request.user.is_staff:
        try:
            quiz = get_object_or_404(Quiz, id=quizID)
            try:
                scores = get_list_or_404(Score, quiz=quizID)
            except:
                scores = ''
        except Http404:
            messages.error(
                request, 'Error in finding quiz - speak to admin')
            return redirect('quizzes')

        if request.method == 'POST':
            form = quizForm(request.POST or None,
                            request.FILES or None, instance=quiz)
            if form.is_valid():
                form.save()
                return redirect('quizzes')
        try:
            questionList = get_list_or_404(Question, quiz=quizID)
        except Http404:
            questionList = ''
        # checks if questionList exisits
        data = {
            'title': quiz.title,
            'classes': quiz.classes,
            'level': quiz.level,
            'image_path': quiz.image_path,
        }
        preFilledForm = quizForm(initial=data)
        context = {
            'form': preFilledForm,
            'id': quizID,
            'questions': questionList,
            'scores': scores,
        }
        return render(request, 'quiz/createQuiz.html', context)
    messages.error(
        request, 'You are not authenticated')

    return redirect('index')


def updateQuestion(request, questionID):
    if request.user.is_authenticated & request.user.is_staff:
        question = get_object_or_404(Question, id=questionID)
        if request.method == 'POST':
            form = questionForm(request.POST or None,
                                request.FILES or None, instance=question)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        try:
            questionList = get_list_or_404(Question, quiz_id=question.quiz_id)
            filtered_QuestionList = [
                value for value in questionList if not value.id == questionID]
            data = {
                'title': question.title,
                'answer_1': question.answer_1,
                'answer_2': question.answer_2,
                'answer_3': question.answer_3,
                'answer_4': question.answer_4,
                'correct_answer': question.correct_answer,
                'image_path': question.image_path,
            }
            preFilledForm = questionForm(initial=data)
            context = {
                'form': preFilledForm,
                'id': questionID,
                'quiz_id': question.quiz_id,
                'questions': filtered_QuestionList,
            }
            return render(request, 'question/question.html', context)
        except Http404:
            messages.error(
                request, 'could not find questions - speak to admin')

            return redirect('index')
    return redirect('index')


def submit(request):
    # TODO make it so if the question is wrong -- add it to a dict and show on page.
    if request.method == 'POST':
        score = 0
        question = {}
        wrongAnswerList = []
        submitted = {answer: request.POST[answer] for answer in request.POST.keys(
        ) - {'csrfmiddlewaretoken', 'id'}}

        for id in submitted:
            question = get_object_or_404(Question, id=id)
            if (str(question.correct_answer) == submitted[id]):
                score = score + 1
            else:
                wrongAnswerList.append(question)
        try:
            quizValues = get_object_or_404(Quiz, pk=question.quiz.pk)
            Score.objects.create(score=score, quiz=quizValues, teacher=quizValues.teacher,
                                 first_name=request.user.first_name, last_name=request.user.last_name)
        except Http404:
            messages.error(
                request, 'Error in sending results - speak to admin')
            return redirect('quizzes')
        # submitScore.save()
        context = {
            'wrongAnswer': wrongAnswerList,
            'score': score
        }
        return render(request, 'quiz/submitted.html', context)
    return redirect('quizzes')

    # try: looping dict useful

    #     question = Question.objects.get(id=questionID)

    #     formatted_values = {value: request.POST[value] for value in request.POST.key(

    #     ) - {'csrfmiddlewaretoken', 'id'}}

    #     for key in formatted_values:

    #         question.key = formatted_values[key]

    #     print(question)

    #     return redirect('quizzes')

    # except Http404:

    #     return redirect('index')
