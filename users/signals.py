from django.db.models.signals import post_save, post_delete #django signals
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings

#function that create new profile after new user registration
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email = user.email,
            name=user.first_name,
        )

        subject = 'Welcome to DevSearch!'
        message = 'We are glad you are here!'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    
    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.wmail = profile.email
        user.save()


#delete user after deleting profile
def deleteUser(sender, instance, **kwargs): 
    try:
        user = instance.user
        user.delete()
    except:
        pass
 
post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender = Profile)
post_delete.connect(deleteUser, sender=Profile)