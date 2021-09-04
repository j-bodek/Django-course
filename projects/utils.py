from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(request, projects, results_per_page):

    page = request.GET.get('page')
    paginator = Paginator(projects, results_per_page)

    try:
        projects = paginator.page(page) 

    except PageNotAnInteger: # if user goes to first page
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages #if user get for example 100 page display him last one
        projects = paginator.page(page)


    leftIndex = (int(page)-1)
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 2)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custome_range = range(leftIndex, rightIndex)

    return custome_range, projects

def searchProjects(request):

    search_quary = ''

    if request.GET.get('text'):
        search_quary = request.GET.get('text')

    tags = Tag.objects.filter(name__icontains=search_quary)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_quary) |
        Q(description__icontains=search_quary) |
        Q(owner__name__icontains=search_quary) | # every project when owner name contains sarch_quary
        Q(tags__in=tags)
    )

    return search_quary, projects


