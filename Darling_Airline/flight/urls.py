from django.urls import path

from . import views

urlpatterns =[
    path('',views.index, name='index'),
    path('signup/', views.save, name='signUp'),
    path('login/', views.signin, name='login'),
    path('profile/', views.profile, name='profile'),
    path('account/', views.logout, name='logout'),
]