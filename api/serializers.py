from rest_framework import serializers
from projects.models import Project

# that's gonna convert project model into json object
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project 
        fields = '__all__' 