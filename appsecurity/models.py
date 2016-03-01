from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib import admin

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger()

class UserProfile(models.Model):
        
    user = models.OneToOneField(User)
    activation_key = models.CharField(null=True, blank=True, max_length=256)
    key_expires=models.DateTimeField(null=True, blank=True)

admin.site.register(UserProfile)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        #UserProfile.objects.create(user=instance)
        
post_save.connect(create_user_profile, sender=User)