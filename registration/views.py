from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from registration.forms import SignUpForm
from registration.models import MyUser
from registration.tokens import account_activation_token


def home(request):
    return render(request, 'registration/home.html')


def home_logout(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            my_user = form.save(commit=False)
            my_user.user.is_active = False

            my_user.save()
            current_site = get_current_site(request)

            message = render_to_string(
                'registration/account_activation_email.html', {
                    'user': my_user.user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(
                        force_bytes(my_user.pk)).decode(
                        "utf-8"),
                    'token': account_activation_token.make_token(my_user),
                })

            subject = 'Ative sua conta no DeGRSys.ga'
            my_user.user.email_user(subject, message,
                                    from_email=settings.PROJECT_EMAIL)

            return render(request, 'registration/account_activation_sent.html',
                          {'user': my_user.user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        my_user = MyUser.objects.get(pk=uid)
        user = my_user.user
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        my_user = None
        user = None

    if user is not None and account_activation_token.check_token(my_user,
                                                                 token):
        user.is_active = True
        user.save()

        my_user.email_confirmed = True
        my_user.save()

        login(request, user)
        return redirect('user_home')
    else:
        return render(request, 'registration/account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')


def login_redirect(request):
    user = request.user
    if user is not None:
        if user.is_active:
            if user.is_superuser or user.is_staff:
                return HttpResponseRedirect('/admin')
            else:
                return redirect('user_home')
        else:
            pass
    # Return a 'disabled account' error message
    else:
        pass
# Return an 'invalid login' error message.
