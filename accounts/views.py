from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy


def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/")
                else:
                    message = 'Disabled account'
            else:
                message = 'Invalid login'

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'login_form': form, 'message': message})


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def signup(request):
    signup_form = RegisterForm(request.POST or None)
    if signup_form.is_valid():
        signup_form.save()
        return redirect("/")
    context = {
        'form': signup_form
    }
    return render(request, 'accounts/signup.html', context)


class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('logout')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
