from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile



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
    # # if user sent a form
    # if request.method == "POST":
    #     # take email from form
    #     email = request.POST['email']
    #     # try to send password to email
    #     try:
    #         msg = EmailMessage()
    #         msg['Subject'] = 'Test'
    #         msg['From'] = 'admin@cv-it.ru'
    #         msg['To'] = 'loolikwoow@gmail.com'
    #         msg.set_content('Test email')
    #         server = smtplib.SMTP_SSL('smtp.timeweb.ru', 465)
    #         server.login('admin@cv-it.ru', 'Lolikwoow123')
    #         server.send_message(msg)
    #         server.quit()
    #
    #         mail = EmailMessage('Successfully registered', f'Hello! Your account has been successfully registered. '
    #                                                        f'\n\nYour password is: \n\t{password}\nYou can change your '
    #                                                        f'password in profile page!\n\n\n All the best !',
    #                             to=[email])
    #         # we calling function 'sent' 3 times, because sometimes it dosent work
    #         mail.send()
    #         mail.send()
    #         mail.send()
    #         # create a user with email and password that we generate
    #         User.objects.create_user(username=email, password=password, email=email)
    #         # ok massage for home page
    #         messages.success(request,
    #                          f'Your account has been successfully registered. Your password has been sent to your eamil address')
    #     except:
    #         # ERROR massage for home page
    #         messages.error(request, f'Something went wrong with creating a new account. Try again later.')
    #         # open a register page (link) again
    #         return render(request, 'users/registraion.html')
    #     # if we took a form and it was registered successfully, open a home page
    #     return redirect('log')
    # # if user just opened a register page, but didnt submit a form yet, just open register page
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
