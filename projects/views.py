from django.shortcuts import redirect, render, redirect
from django.contrib.auth.decorators import login_required 

# Create your views here.

from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm


def projects(request):
    projects = Project.objects.all()
    context = {'projects':projects}
    return render(request, 'projects/projects.html', context)

def project(request, project_id):
    projectObj = Project.objects.get(id=project_id)
    return render(request, 'projects/single-project.html', {'project': projectObj})

@login_required(login_url='login') #only login users can display this
def create_project(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url='login')
def update_project(request, project_id):
    project = Project.objects.get(id=project_id)
    form = ProjectForm(instance = project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url='login')
def deleteProject(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    context = {'object':project}
    return render(request, 'projects/delete_template.html', context)