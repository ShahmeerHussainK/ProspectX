from rest_framework import serializers
from .models import *


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'list_name', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag_name', 'created_at']


class CustomFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFieldsModel
        fields = '__all__'


class ProspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prospect_Properties
        fields = '__all__'


class ProspectListsSerializer(serializers.ModelSerializer):
    list = ListSerializer()

    class Meta:
        model = Prospect_Properties
        fields = ['list', ]


class ProspectTagsSerializer(serializers.ModelSerializer):
    tag = TagSerializer()

    class Meta:
        model = Prospect_Properties
        fields = ['tag', ]



