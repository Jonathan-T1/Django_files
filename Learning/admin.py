from django.contrib import admin
from .models import User ,Task, Cohorte

# Register your models here.

admin.site.register(User),
admin.site.register(Cohorte)