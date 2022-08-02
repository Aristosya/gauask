from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .models import Question
from users.models import Profile
import smtplib
from email.message import EmailMessage


def homePage(request):
    if request.user.is_authenticated:
        if request.user.profile.teacher:
            questions = Question.objects.filter(teacher=request.user, isDone=False).all()
            settings = {
                'questions': questions
            }
            return render(request, 'application/home_teacher.html', settings)

    teachers = Profile.objects.filter(teacher=True).all()
    settings = {
        'teachers':teachers,
    }
    return render(request, 'application/home.html',settings)




def aboutPage(request):
    return render(request, 'application/about.html')


@login_required
def createQuestion(request, teacher):
    teacher = get_object_or_404(User, id=teacher)
    if teacher.profile.teacher:
        if request.method == "POST":
            title = request.POST['title']
            question = request.POST['question']
            Question.objects.create(title=title, student=request.user, question=question, teacher=teacher, answer='')
            messages.success(request, "Question created successfully")
            return redirect('questions')
        settings = {
            'teacher': teacher,
        }
        return render(request, 'application/create_question.html', settings)
    return redirect('home')


@login_required
def createTeacher(request):
    if request.user.is_staff:
        if request.method == 'POST':
            first_name = request.POST['name']
            last_name = request.POST['surname']
            email = request.POST['email']
            try:
                msg = EmailMessage()
                msg['Subject'] = 'GauAsk Password'
                msg['From'] = 'admin@gauask.com'
                msg['To'] = email
                msg.set_content('Your password is TeacherGauAsk2022*')
                server = smtplib.SMTP_SSL('smtp-muhammed123123.alwaysdata.net', 465)
                server.login('admin@gauask.com', 'GL>32yAV')
                server.send_message(msg)
                server.quit()
                    # create a user with email and password that we generate
                User.objects.create_user(username=email, password='TeacherGauAsk2022*', email=email, first_name=first_name,last_name=last_name)
                newuser = User.objects.filter(username=email).first()
                newuser.profile.teacher = True
                newuser.save()
                    # ok massage for home page
                messages.success(request, f'Password has been sent to email')
            except:
                messages.error(request, f'Something went wrong')
        return render(request, 'application/create_teacher.html')
    return redirect('home')


@login_required
def questions(request):
    if request.user.profile.teacher:
        return redirect('home')
    questions = Question.objects.filter(student=request.user).all()
    settings = {
        'questions': questions,
    }
    return render(request, 'application/my_questions.html',settings)


@login_required
def answerQuestion(request, id):
    if request.user.profile.teacher:
        question = get_object_or_404(Question, id=id)
        if question.teacher == request.user:
            settings = {
                'question': question,
            }
            return render(request, 'application/answer_question.html',settings)
    return redirect('home')


@login_required
def answeredQuestion(request, id, buttonId):
    if request.user.profile.teacher:
        question = get_object_or_404(Question, id=id)
        if question.teacher == request.user:
            if request.method == "POST":
                question.answer= request.POST['answer']
                if buttonId == 1:
                    status = 'Answered'
                    question.isDone = True
                elif buttonId == 2:
                    status = 'Evaluated'
                elif buttonId == 3:
                    status = 'Discarded'
                    question.isDone = True
                else:
                    status = 'Not read yet'
                question.status = status
                question.save()
    return redirect('home')