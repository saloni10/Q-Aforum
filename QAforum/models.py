from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Question(models.Model):
   
    user_id = models.ForeignKey(User)
    title = models.CharField(max_length=60)
    date_created = models.DateField(max_length=30)
    date_update = models.DateField(max_length=50)
    is_anonymous = models.BooleanField(default=False)
    def __unicode__(self):
        return self.title
