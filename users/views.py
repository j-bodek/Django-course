from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from .forms import CustomUserCreationForm

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
            return redirect('profiles')

        else:
            messages.error(request, 'An error has occured during registration')

    context = {'page':page, 'form':form}
    return render(request, 'users/login_register.html', context)


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