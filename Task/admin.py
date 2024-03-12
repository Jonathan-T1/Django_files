from django.contrib import admin

# Register your models here.
from .models import Task,Calificacion

admin.site.register(Task),
admin.site.register(Calificacion),