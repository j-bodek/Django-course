from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name="projects"), 
    path('project/<str:project_id>/', views.project, name="project"), 
    path('create-project/', views.create_project, name='create-project'),
    path('update-project/<str:project_id>/', views.update_project, name='update-project'),
    path('delete-project/<str:project_id>/', views.deleteProject, name='delete-project'),
]