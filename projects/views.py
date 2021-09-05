from projects.utils import searchProjects
from django.shortcuts import redirect, render, redirect
from django.contrib.auth.decorators import login_required 

# Create your views here.

from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects


def projects(request):

    search_quary, projects = searchProjects(request)
    custome_range ,projects = paginateProjects(request, projects, 3)


    context = {'projects':projects, 'search_quary':search_quary, 'custome_range':custome_range}
    return render(request, 'projects/projects.html', context)


def project(request, project_id):
    projectObj = Project.objects.get(id=project_id)
    form = ReviewForm()
    return render(request, 'projects/single-project.html', {'project': projectObj, 'form': form})



@login_required(login_url='login') #only login users can display this
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form': form}
    return render(request, "projects/project_form.html", context)



@login_required(login_url='login')
def update_project(request, project_id):
    profile = request.user.profile
    project = profile.project_set.get(id=project_id) #set all project of login user
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
    profile = request.user.profile
    project = profile.project_set.get(id=project_id) #set all project of login user
    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    context = {'object':project}
    return render(request, 'delete_template.html', context)