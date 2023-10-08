from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.todo_list, name='todo-list'),
    path('todos/<int:id>/', views.delete_todo, name='delete-todo'),
    path('todos/<int:id>/<str:status>/',
         views.update_todo_status, name='update-todo-status'),
    path('create-todo/', views.create_todo, name='create-todo'),
    path('register/', views.register_user, name='register-user'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
