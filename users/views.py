from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from users.forms import UserSignUpForm
from users.models import CustomUser


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()

        context = {
            'login_form':login_form,
        }
        return render(request, 'users/login.html', context)
    def post(self, request):
        login_form = AuthenticationForm(data = request.POST)

        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        usernomi = username.lower()
        user = authenticate(request, username=usernomi, password=password)
        if user is not None:
                login(request, user)
                messages.success(request, "Siz muvaffaqiyatli - Akkauntingizga kirdingiz!")
                return redirect('film:profile')  # 'home' - sizning bosh sahifangizni nomi

        messages.error(request, 'Login yoki parol xato!')
        context = {
            'login_form': login_form,
        }
        return render(request, 'users/login.html', context)


#SIGN UP
class SignUpPageView(View):
    def get(self, request):
        create_form = UserSignUpForm()
        context = {
            "signup_form": create_form
        }
        return render(request, 'users/signup.html', context)

    def post(self, request):
        create_form = UserSignUpForm(data=request.POST)

        if create_form.is_valid():
            user = create_form.save()
            login(request, user)
            messages.success(request, "Siz muvaffaqiyatli - Ro'yxatdan o'tdingiz")
            return redirect("film:profile")
        else:
            context = {
                "signup_form": create_form
            }
            return render(request, 'users/signup.html', context)


class LogoutPageView(LoginRequiredMixin, View):
    def get(self, request):

        return render(request, 'users/logout.html')


class LoggedoutPageView( LoginRequiredMixin, View,):
    def get(self, request):
            logout(request)
            messages.warning(request, "Siz akkauntingizdan chiqib ketdingiz")
            return redirect("film:home")