from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
import smtplib
from email.message import EmailMessage




# To change old password
@login_required
def changePassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        user = get_object_or_404(User, id= request.user.id)
        user.set_password(password)
        user.save()
        messages.success(request, f'Your password has been changed.')
        return redirect('logIn')
    return render(request, 'users/change_password.html')


# registration backend
def registration(request):
    # if user sent a form
    if request.method == "POST":
        # take email from form
        first_name = request.POST['name']
        last_name = request.POST['surname']
        email = f'{first_name}.{last_name}@std.gau.edu.tr'
        # try to send password to email
        try:
            msg = EmailMessage()
            msg['Subject'] = 'GauAsk Password'
            msg['From'] = 'admin@gauask.com'
            msg['To'] = email
            msg.set_content('Your password is GauAsk2022*')
            server = smtplib.SMTP_SSL('smtp-muhammed123123.alwaysdata.net', 465)
            server.login('admin@gauask.com', 'GL>32yAV')
            server.send_message(msg)
            server.quit()
            # create a user with email and password that we generate
            User.objects.create_user(username=email, password='GauAsk2022*', email=email, first_name = first_name, last_name = last_name)
            # ok massage for home page
            messages.success(request,f'Your password has been sent to email')
        except:
            # ERROR massage for home page
            messages.error(request, f'Something went wrong')
            # open a register page (link) again
            return render(request, 'users/registration.html')
        # if we took a form and it was registered successfully, open a home page
        return redirect('logIn')
    # if user just opened a register page, but didnt submit a form yet, just open register page
    return render(request, 'users/registration.html', )


@login_required
def changeImage(request):
    # if user sent a form
    if request.method == "POST":
        # take from files input our photo
        main_photo = request.FILES.get('main_photo')
        # chek if its empty
        if main_photo:
            # Take profile object of this user who did request
            profile = get_object_or_404(Profile, user = request.user)
            # change profile image to new one
            profile.img = main_photo
            # save to Database
            profile.save()
            # success message to page
            messages.success(request, f'Your image has been successfully updated')
        else:
            messages.success(request, f'You didnt upload image')
        # when its done open change image page
        return redirect('changeImage')
    # else => user didnt submit form yet
    else:
        # take a picture that already in system
        img_profile = Profile.objects.filter(user=request.user).first()
    # data for frontend
    data = {
        'img_profile': img_profile,
    }
    # open change image page
    return render(request, 'users/change_image.html', data)
