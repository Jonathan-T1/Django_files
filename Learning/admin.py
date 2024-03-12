from django.contrib import admin
from .models import User, Cohorte,Profile,Registration


# Register your models here.

admin.site.register(User),

class CourseAdmin(admin.ModelAdmin):
    list_display=('nombreCoh','teacher',)
    list_filter=('teacher',)
admin.site.register(Cohorte,CourseAdmin),

class ResgistracionAdmin(admin.ModelAdmin):
    list_display=('course','student')
    list_filter=('course','student')
admin.site.register(Registration,ResgistracionAdmin),

admin.site.register(Profile),





    
"""
class CursoAdmin(admin.ModelAdmin):
    list_display=('nombre','lecciones')
    list_filter=('nombre','lecciones')
admin.site.register(Cursos,CursoAdmin),
"""
