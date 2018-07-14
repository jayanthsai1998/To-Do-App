from rest_framework import status
from rest_framework.response import Response
from todolistapp.serializers import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


"""
API VIEWS
"""


class ApiToDoListItemListView(APIView):
    def get(self, request, **kwargs):
        todolistitems = ToDoListItem.objects.filter(**kwargs)
        serializer = ToDoListItemSerializer(todolistitems, many=True)
        return Response(serializer.data)

    def post(self, request, **kwargs):
        serializer = ToDoListItemSerializer(data={**request.data, **kwargs})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiToDoListItemDetails(APIView):
    def get(self, request, **kwargs):
        todolistitem = get_object_or_404(ToDoListItem, **kwargs)
        serializer = ToDoListItemSerializer(todolistitem)
        if not serializer:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

    def put(self, request, **kwargs):
        todolistitem = get_object_or_404(ToDoListItem, **kwargs)
        serializer = ToDoListItemSerializer(todolistitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        todolistitem = get_object_or_404(ToDoListItem, **kwargs)
        todolistitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
