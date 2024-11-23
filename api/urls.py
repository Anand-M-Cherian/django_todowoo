from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('signup', views.signup),
    path('login', views.login),

    # ToDos
    path('todos', views.ListCreateTodo.as_view()),
    path('todos/<int:pk>', views.GetUpdateDeleteTodo.as_view()),
    path('todos/<int:pk>/complete', views.CompleteTodo.as_view()),
    path('todos/<int:pk>/undo', views.UndoCompleteTodo.as_view()),
    path('todos/completed', views.ListCompletedTodos.as_view()),
]