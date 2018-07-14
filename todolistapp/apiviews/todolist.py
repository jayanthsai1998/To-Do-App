from rest_framework import status
from rest_framework.response import Response
from todolistapp.serializers import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class ApiToDoListView(APIView):
    def get(self, request, **kwargs):
        todolists = ToDoList.objects.filter(user=request.user)
        serializer = ToDoListSerializer(todolists, many=True)
        return Response(serializer.data)

    def post(self, request, **kwargs):
        serializer = ToDoListSerializer(data={**request.data, **kwargs})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApiToDoListDetails(APIView):
    def get(self, request, **kwargs):
        todolist = get_object_or_404(ToDoList, **kwargs)
        serializer = ToDoListSerializer(todolist)
        if not serializer:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

    def put(self, request, **kwargs):
        todolist = get_object_or_404(ToDoList, **kwargs)
        serializer = ToDoListSerializer(todolist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        todolist = get_object_or_404(ToDoList, **kwargs)
        todolist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)