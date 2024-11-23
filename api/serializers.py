from rest_framework import serializers
from todo.models import Todo

class ToDoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    datecompleted = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ['id','title','memo','created','datecompleted','important']

class CompleteToDoSerializer(serializers.ModelSerializer):
    # all fields are read only. user should not be able to change anything

    class Meta:
        model = Todo
        fields = ['id']
        read_only_fields = ['title','memo','created','datecompleted','important']