from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, profiles, results_per_page):

    page = request.GET.get('page')
    paginator = Paginator(profiles, results_per_page)

    try:
        profiles = paginator.page(page) 

    except PageNotAnInteger: # if user goes to first page
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages #if user get for example 100 page display him last one
        profiles = paginator.page(page)


    leftIndex = (int(page)-1)
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 2)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custome_range = range(leftIndex, rightIndex)

    return custome_range, profiles


def searchProfiles(request):
    search_quary = ''

    if request.GET.get('text'):
        search_quary = request.GET.get('text')

    skills = Skill.objects.filter(name__icontains=search_quary)


    #distinct() makes shure that we didn't have any duplicates
    profiles = Profile.objects.distinct().filter( # Q is like or operator in python
        Q(name__icontains=search_quary) | 
        Q(short_intro__icontains=search_quary) |
        Q(skill__in=skills)) #get all profiles

    return profiles, search_quary

