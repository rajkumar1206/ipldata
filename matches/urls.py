from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.matches_list.as_view(), name='index'),
    path('<int:pk>/list/', views.matches_list_season.as_view(), name='index'),
    path('season/list/', views.season_list.as_view(), name='index'),
    path('add/season/', views.add_season.as_view(), name='index'),
    path('add/user/', views.create_user.as_view(), name='index'),
    path('add/', views.add_match.as_view(), name='index'),
    path('', views.index, name='index'),
]