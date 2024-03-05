from django.contrib import admin
from .models import User ,Task, Cohorte,Profile,Signature,Registration

# Register your models here.

admin.site.register(User),

class CourseAdmin(admin.ModelAdmin):
    list_display=('nombreCoh','teacher',)
    list_filter=('teacher',)
admin.site.register(Cohorte,CourseAdmin),

class ResgistracionAdmin(admin.ModelAdmin):
    list_display=('course','student')
    list_filter=('course','student')
admin.site.register(Registration,ResgistracionAdmin)

admin.site.register(Signature),
admin.site.register(Profile),
admin.site.register(Task)
