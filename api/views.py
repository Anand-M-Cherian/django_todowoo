from rest_framework import generics, permissions
from .serializers import ToDoSerializer, CompleteToDoSerializer
from todo.models import Todo
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Create your views here.

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({'error':'That username has already been taken. Please choose a new username'}, status=400)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            return JsonResponse({'error':'Login Failed. Please check credentials'}, status=400)
        else:
            try:
                token = Token.objects.get(user=user)
                status = 200
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
                status = 201
        return JsonResponse({'token':str(token)}, status=status)

class ListCompletedTodos(generics.ListAPIView):
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        todo = Todo.objects.filter(user=user, datecompleted__isnull=False).order_by('-datecompleted')
        return todo
    
class ListCreateTodo(generics.ListCreateAPIView):
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        todo = Todo.objects.filter(user=user, datecompleted__isnull=True)
        return todo
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GetUpdateDeleteTodo(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        todo = Todo.objects.filter(user=user)
        return todo
    
class CompleteTodo(generics.UpdateAPIView):
    serializer_class = CompleteToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        todo = Todo.objects.filter(user=user)
        return todo
    
    def perform_update(self, serializer):
        serializer.instance.datecompleted = timezone.now()
        serializer.save()

class UndoCompleteTodo(generics.UpdateAPIView):
    serializer_class = CompleteToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        todo = Todo.objects.filter(user=user)
        return todo
    
    def perform_update(self, serializer):
        serializer.instance.datecompleted = None
        serializer.save()