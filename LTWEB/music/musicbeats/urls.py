from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('songs/', views.songs, name="songs"),
    path('songs/<int:id>', views.songpost, name="songpost"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('watchlater/',views.watchlater, name="watchlater"),

]
