from django.shortcuts import render
from .models import Profile

# Create your views here.


def profiles(request):
    profiles = Profile.objects.all() #get all profiles
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk) #get single profile by id value

    topskills = profile.skill_set.exclude(description__exact="") #exclude all skills that didn't have description 
    otherskills =profile.skill_set.filter(description="") #include all skills that dind't have description
    context = {'profile':profile, 'topskills':topskills, 'otherskills':otherskills}
    return render(request,'users/user_profile.html', context)