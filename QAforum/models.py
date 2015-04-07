from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db.models import Count 

# Create your models here.

        
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='.', blank=True, default='/media/default_user.jpg')
    
    

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class Question(models.Model):
   
    user_id = models.ForeignKey(User)
    
    title = models.CharField(max_length=60)
    date_created = models.DateField(max_length=30)
    date_update = models.DateField(max_length=50)
    is_anonymous = models.BooleanField(default=False)
    
    def num_posts(self):
        return self.id.Count(pk=user_id)
        
    def __unicode__(self):
        return self.title
        
