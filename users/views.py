from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from .forms import CustomUserCreationForm, Profileform, SkillForm
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
from .utils import searchProfiles, paginateProfiles

# Create your views here.

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated: #if user is login redirect him to profiles page
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        

        try:
            user = User.objects.get(username=username) #chaeck if user exist in database
        except:
            messages.error(request, 'username does not exist')
            

        user = authenticate(request, username=username, password=password) # it make sure if password matches the username

        if user:
            login(request, user) #this create user session in database
            return redirect('profiles') #redirect user
        else:
             messages.error(request, 'Username or password is incorrect')
        

    return render(request, 'users/login_register.html')


def logoutUser(request): 
    logout(request)
    messages.error(request, 'User logout')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit_account')

        else:
            messages.error(request, 'An error has occured during registration')

    context = {'page':page, 'form':form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    
    profiles, search_quary = searchProfiles(request)

    custome_range, profiles = paginateProfiles(request, profiles, 3)

    context = {'profiles': profiles, 'search_quary':search_quary, 'custome_range':custome_range}
    return render(request, 'users/profiles.html', context)



def userProfile(request, pk):
    profile = Profile.objects.get(id=pk) #get single profile by id value

    topskills = profile.skill_set.exclude(description__exact="") #exclude all skills that didn't have description 
    otherskills =profile.skill_set.filter(description="") #include all skills that dind't have description
    context = {'profile':profile, 'topskills':topskills, 'otherskills':otherskills}
    return render(request,'users/user_profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile':profile, 'skills':skills, 'projects':projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = Profileform(instance=profile)

    if request.method == 'POST':
        form = Profileform(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form':form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()

            messages.success(request, 'Skill was created successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)



@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()

            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')

    context = {'object':skill}
    return render(request, 'delete_template.html', context)