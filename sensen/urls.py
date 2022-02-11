from django.urls import path
from .views import *


urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('register/',RegistrationView,name='register'),
    path('login/',LoginView,name='login'),
    path('logout/',LogoutView,name='logout'),
    path('show/',ShowBlogs,name='show'),
    path('add/',AddNewBlog,name='blog'),
    path('delete/<int:id>/',DeleteView,name='delete'),
    path('blogdetails/<slug:slug>',BlogDetailView.as_view(),name= 'blogdetail'),
    path('addshow/',AddShow,name='addshow'),
    path('search/',SearchView.as_view(),name='search'),
    path('profile/',CustomerProfile.as_view(),name='profile'),
    path('forgot-password/',PasswordForgot.as_view(),name="forgetpassword"),
    
]