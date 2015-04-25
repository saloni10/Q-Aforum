from django.contrib import admin

# Register your models here.
from models import *
admin.autodiscover()
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserProfile)