from django.contrib import admin
from eaecontrol import models
# Register your models here.

admin.site.register(models.Person)
admin.site.register(models.Timing)
admin.site.register(models.Group)