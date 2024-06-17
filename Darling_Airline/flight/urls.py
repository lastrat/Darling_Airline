from django.urls import path
from . import api_views

from . import views

urlpatterns =[
    path('',views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('api/signup/', api_views.signup, name='api_signup'),
    path('api/login/', api_views.login, name='api_login'),
    path('home/', views.home, name='home'),
    path('stops/', views.stops, name='stops'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('flights/', views.flights, name='flights'),
    path('contact/', views.contact, name='contact'),
    path('reservation/',views.reservation, name='reservation'),
    path('myreservations/', views.myreservations, name='myreservations'),
    path('payment/',views.payment, name='payment'),
    path('ticket/',views.ticket, name='ticket'),
]