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


@login_required
def createQuestion(request, teacher):
    teacher = get_object_or_404(User, id=teacher)
    if teacher.profile.teacher:
        if request.method == "POST":
            title = request.POST['title']
            question = request.POST['question']
            Question.objects.create(title=title, student=request.user, question=question, teacher=teacher, answer='')
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


@login_required
def viewTicketPage(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    isCreator, isLecturer = False, False
    if request.user == ticket.creator:
        isCreator = True
        ticket.isNotification = False
        ticket.save()
    if request.user == ticket.lecturer.lecturer:
        isLecturer = True
    if isCreator or isLecturer:
        settings = {
            'isLecturer': isLecturer,
            'ticket': ticket,
        }
        return render(request, 'application/view_ticket.html', settings)
    return redirect('home')


@login_required
def answerTicketPage(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    isLecturer = False
    if request.user == ticket.lecturer.lecturer:
        isLecturer = True
    if not isLecturer:
        return redirect('home')
    if request.method == 'POST':
        status = request.POST['status']
        answer = request.POST['answer']
        ticket.answer = answer
        ticket.status = status
        if status != 'NR':
            ticket.isNotification = True
        ticket.save()
        return redirect('ticket-view', id)

    settings = {
        'isLecturer': isLecturer,
        'ticket': ticket,
    }
    return render(request, 'application/answer_ticket.html', settings)


@login_required
def createLecturer(request):
    lecturer = Lecturer.objects.filter(lecturer=request.user).first()
    if lecturer is None or not lecturer:
        isLecturer = False
    else:
        isLecturer = True
    # if user is not admin - go to home page
    if not request.user.is_superuser:
        return redirect('home')
    # if user sent a form
    if request.method == "POST":
        # take email from form
        email = request.POST['email']
        # generate a password
        password = pwo.generate()
        # try to send password to email
        try:
            mail = EmailMessage('You registred as lecturer',
                                f'Hello! Your account has been successfully registered like a lecturer. '
                                f'\n\nYour password is: \n\t{password}\nYou can change your '
                                f'password in profile page!\n\n\n All the best !',
                                to=[email])
            # we calling function 'sent' 3 times, because sometimes it dosent work
            mail.send()
            mail.send()
            mail.send()
        except:
            # ERROR massage for home page
            messages.error(request, f'Something went wrong with creating a new account. Try again later.')
            # open a register page (link) again
            return render(request, 'application/create_lecturer.html')
        # create a user with email and password that we generate
        newUser = User.objects.create_user(username=email, password=password, email=email)
        newLecturer = Lecturer.objects.create(lecturer=newUser)
        # ok massage for home page
        messages.success(request,
                         f'New lecturer has been created password sent to eamil address')
        # if we took a form and it was registered successfully, open a home page
        return redirect('home')
    # if user just opened a register page, but didnt submit a form yet, just open register page
    settings = {
        'isLecturer': isLecturer,
    }
    return render(request, 'application/create_lecturer.html', settings)
