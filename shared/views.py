from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from film.models import FilmModel
from shared.forms import FeedbackForm
from shared.models import MurojaatModel
from users.models import CustomUser


class Admin(View):

    def get(self, request):
        admin_users = CustomUser.objects.filter(is_superuser=True)
        feedbacks = MurojaatModel.objects.all().order_by("-publish_time")
        context = {
            'admin_users':admin_users,
            "feedbacks":feedbacks,
        }
        return render(request, 'shared/admin.html', context)

class AllUsers(View):
    def get(self, request):
        users = CustomUser.objects.all().order_by("-date_joined")

        context = {
            'users':users
        }
        return render(request, 'shared/allusers.html', context)




class DMCA(View):
    def get(self, request):
        return render(request, 'shared/dmca.html')

class DMCAru(View):
    def get(self, request):
        return render(request, 'shared/dmcaru.html')

class Feedback(LoginRequiredMixin, View):
    def get(self, request):
        form = FeedbackForm()
        context = {
            'form':form,
        }
        return render(request, 'shared/feedback.html', context)

    def post(self, request):
        form = FeedbackForm(data=request.POST)
        form.user = request.user
        feedbackall = MurojaatModel.objects.all()
        if form.is_valid():
            if not feedbackall.count() > 100:
                murojaat = MurojaatModel(user=request.user, title=form.cleaned_data['title'], body=form.cleaned_data['body'],)
                murojaat.save()
                messages.success(request, "Xabar yuborildi. Tez orada javob beramiz")
                return redirect("film:home")
            else:
                messages.error(request, "Xabar yuborilmadi! Haddan tashqari ko'p xabar keldi!")
                return redirect("film:home")

        context = {
            'form': form,
        }
        return render(request, 'shared/feedback.html', context)

class ads_view(View):
    def get(self, request):
        return render(request, 'shared/ads.html')\

class About(View):
    def get(self, request):
        return render(request, 'shared/about.html')

class Foydalan(View):
    def get(self, request):
        return render(request, 'shared/foydalan.html')

class CreateWeb(View):
    def get(self, request):

        return render(request, 'shared/create_web.html')