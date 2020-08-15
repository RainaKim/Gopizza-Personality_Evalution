from django.urls import path
from . import views

urlpatterns = [
    path('',views.registration),
    path('/verify', views.token_verification),
    path('/admin/sign-up', views.admin_signup),
    path('/admin/sign-in', views.admin_signin),
]
