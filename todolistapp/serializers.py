from todolistapp.models import *
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.utils.six import BytesIO


class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = ('id', 'name')

    def create(self, validated_data):
        validated_data.pop('id')
        return ToDoList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        return instance


class ToDoListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoListItem
        fields = ('id', 'content', 'finished', 'date_created')

    def create(self, validated_data):
        validated_data.pop('id')
        todolisitem = ToDoListItem(**validated_data)
        todolisitem.todolist = ToDoList.objects.get(id=self._kwargs.get('data').get('todolist_id'))
        todolisitem.save()
        return todolisitem

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.finished = validated_data.get('finished', instance.finished)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        return instance