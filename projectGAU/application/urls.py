from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),  # Url pattern for the home page
    path('question/create/<int:teacher>', views.createQuestion, name='createQuestion'),
    path('questions/', views.questions, name='questions'),
    path('/create/teacher', views.createTeacher, name='createTeacher'),
    path('question/answer/<int:id>', views.answerQuestion, name='answerQuestion'),
    path('question/answered/<int:id>/<int:buttonId>', views.answeredQuestion, name='answeredQuestion'),
    path('panel/create-lecturer/', views.createLecturer, name='create-lecturer'),
    path('ticket/<int:id>/', views.viewTicketPage, name='ticket-view'),
    path('ticket/<int:id>/answer/', views.answerTicketPage, name='ticket-answer'),
]
