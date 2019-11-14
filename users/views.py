from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import UserRegisterForm
from .tokens import account_activation_token
from .models import User



def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("USER CORRECT")
            current_site = get_current_site(request)
            subject = "Sign Up on NEWS"
            message = "Thank you for registration on our website. Please confirm your email by clicking on link below."
            message = render_to_string('email/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            from_email = settings.EMAIL_HOST_USER
            to_email = user.email
            email = EmailMessage(subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserRegisterForm()
        return render(request, 'usr/register.html', context={'form': form})

            
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



