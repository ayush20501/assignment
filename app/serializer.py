from rest_framework import serializers
from .models import MarkSheet

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkSheet
        fields = '__all__'

def dynamic_serializer(all_fields):
    class DynamicStudentSerializer(serializers.ModelSerializer):
        class Meta:
            model = MarkSheet
            fields = all_fields

    return DynamicStudentSerializer