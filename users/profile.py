#Profile page codes - View
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.views import View

from film.models import FilmLike, FilmSaved, FilmModel
from users.forms import UserEditForm, PasswordChangeForm
from users.models import CustomUser


class Profile(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("users:login")
        liked = FilmLike.objects.filter(user=request.user, like=True).order_by('-publish_time')
        saved = FilmSaved.objects.filter(user=request.user, saved=True).order_by('-publish_time')

        context = {
          'user':request.user,
            'yoqtirgan':liked,
            'saqlangan':saved,
        }
        return render(request, "users/profile.html", context)


# -*- EDIT -*-
class EditProfile(LoginRequiredMixin, View):
    def get(self, request, ):
        user_form = UserEditForm(instance=request.user)
        liked = FilmLike.objects.filter(user=request.user, like=True).order_by('-publish_time')
        saved = FilmSaved.objects.filter(user=request.user, saved=True).order_by('-publish_time')

        context = {
            "user_form":user_form,
            'yoqtirgan': liked,
            'saqlangan': saved,
            }
        return render(request, 'users/profile_edit.html',context)

    def post(self, request):
        user_update_form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES)
        if user_update_form.is_valid():
            user_update_form.save()
            new_username = user_update_form.cleaned_data['username']
            existing_user = CustomUser.objects.filter(username=new_username)
            if existing_user.exists():  # Bazada bunday username mavjud bo'lsa
                for exis in existing_user:
                    if not exis.second_id == request.user.second_id:
                        return render(request, 'users/profile_edit.html', {'user_form': user_update_form, 'error_message': 'Bu username band. Iltimos boshqa username kiriting!'})
                    else:
                        messages.success(request, "Siz muvaffaqiyatli Profil malumotlarini o'zgartirdingiz.")
                        return redirect("film:profile")
            else:
                messages.success(request, "Siz muvaffaqiyatli Profil malumotlarini o'zgartirdingiz.")
                return redirect("film:profile")
        return render(request, "users/profile_edit.html", {"user_form": user_update_form})


class PasswordChange(LoginRequiredMixin ,View):
    def get(self, request):
        password_form = PasswordChangeForm(instance=request.user)
        liked = FilmLike.objects.filter(user=request.user, like=True).order_by('-publish_time')
        saved = FilmSaved.objects.filter(user=request.user, saved=True).order_by('-publish_time')
        context = {
            "password_form":password_form,
            "saqlangan":saved,
            'yoqtirgan':liked,
        }
        return render(request, 'users/password_change.html', context)
    def post(self, request):
        password_form = PasswordChangeForm(instance=request.user, data=request.POST)

        passwordold = request.POST.get('passwordold')
        user = authenticate(request, username=request.user.username, password=passwordold)
        if user is not None:
                user = password_form.save()
                login(request, user)
                messages.success(request, "Siz muvaffaqiyatli - Parolingizni o'zgartirdingiz!")
                return redirect('film:profile')

        messages.error(request, 'Joriy parolingiz xato kiritilgan!')

        context = {
            "password_form": password_form,
            "error_message":"Joriy parolingiz xato kiritilgan"
        }
        return render(request, 'users/password_change.html', context)