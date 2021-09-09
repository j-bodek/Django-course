from rest_framework.decorators import api_view
from rest_framework.response import Response
from . serializers import ProjectSerializer
from projects.models import Project


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},

        {'POST':'/api/users/token'}, # build in class
        {'POST':'/api/users/token/refresh'}, # build in class 
    ]

    return Response(routes)


@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all() # getting all the projects
    serializer = ProjectSerializer(projects, many=True) #serialize projects

    return Response(serializer.data)



@api_view(['GET'])
def getProject(request, pk):
    projects = Project.objects.get(id=pk) # getting all the projects
    serializer = ProjectSerializer(projects, many=False) #serialize projects

    return Response(serializer.data)