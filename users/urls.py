from django.urls import path

from users.views import SignUpPageView, LoginView, LogoutPageView, LoggedoutPageView

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutPageView.as_view(), name="logout"),
    path('logged/', LoggedoutPageView.as_view(), name='logged'),
    path('signup/', SignUpPageView.as_view(), name="signup"),
]