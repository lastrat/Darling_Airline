from django.urls import path

from . import views

urlpatterns =[
    path('',views.index, name='index'),
    path('signup/', views.save, name='signUp'),
    path('login/', views.signin, name='login'),
    path('home/', views.home, name='home'),
    path('stops/', views.stops, name='stops'),
    path('profile/', views.profile, name='profile'),
    path('account/', views.logout, name='logout'),
    path('flights/', views.flights, name='flights'),
    path('contact/', views.contact, name='contact'),
    path('reservation/',views.reservation, name='reservation'),
]