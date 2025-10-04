from django.urls import path,include
from User import views

urlpatterns = [
    path("", views.signup_view, name="signup"),
    path("verify-otp/", views.verify_otp_view, name="verify_otp"),
    path("login/", views.login_view, name="login"),
    path("Home/", views.home_view, name="home"),
    path("logout/", views.logout_view, name="logout"),
    
    
]
