from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.

class Question(models.Model):
   
    user_id = models.ForeignKey(User)
    title = models.CharField(max_length=60)
    date_created = models.DateField(max_length=30)
    date_update = models.DateField(max_length=50)
    is_anonymous = models.BooleanField(default=False)
    def __unicode__(self):
        return self.title
        
        
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
