from django.contrib import admin
from .models import User ,Task, Cohorte,Profile,Signature

# Register your models here.

admin.site.register(User),
admin.site.register(Cohorte),
admin.site.register(Signature),
admin.site.register(Profile),
admin.site.register(Task)