# This file held all the URL patterns related with user dependencies.
from django.urls import path, include
from users import views as userViews
from django.contrib.auth import views as userDjangoViews

# Url patterns for all user dependencies
urlpatterns = [
    path('registration/', userViews.registration, name='registration'),
    # path('teacher/registration/', userViews.teacherRegistration, name='teacherRegistration'),

    path('change/image/', userViews.changeImage, name='changeImage'),
    path('change/password/', userViews.changePassword, name='changePassword'),
    path('login/', userDjangoViews.LoginView.as_view(template_name='users/logIn.html'), name='logIn'),
    path('signout/', userDjangoViews.LogoutView.as_view(next_page='home'), name='logOut'),
]
