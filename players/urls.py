from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.players_list.as_view(), name='list'),
    path('add/', views.add_player.as_view(), name='add_player'),
    path('details/<int:pk>/', views.player_details.as_view(), name='details'),
    path('update/<int:pk>/', views.update_player.as_view(), name='details'),
    path('delete/<int:pk>/', views.delete_player.as_view(), name='details'),
    path('team/<str:pk>/', views.players_list_by_team.as_view(), name='details'),
    path('', views.index, name='index'),
]