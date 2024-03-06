from django.urls import path
from .views import *
from django.conf import settings
from django.contrib.staticfiles.urls import static



urlpatterns = [
    path('',home,name='home'),
    path('learning/',Learning,name='Learning'),
    path('logout/', exit, name='exit'),
    path('veruser/', datosus, name='see_users'),
    path('Register/', register, name='register'),
    path('ResetPassword/<int:pk>/',Cambiar_contraseña,name='reset_password'),
    path('editaruser/<int:pk>/', editaruser, name='edit_user'),
    path('delete/<int:pk>/',delete_user,name='delete_user'),

#This are the profiles urls 
    path('users/me/profile/',update_profile,name='update_profile'),
    path('users/<str:username>/',UserDetailView.as_view(),name='detail'),
    path('learning/overview/',profile,name='learning_overview'),

#This are the Curses urls
    path('cohorte/',cohorte, name='cohortes'),
    path('crear/curso/',crear_curso,name='crear_curso'),

#This are the task that Cesar did 
    path('tasks/', tasks, name="tasks"),
    path('tasks_completed/', tasks_completed, name="tasks_completed"),
    path('tasks/create/', create_task, name="create_task"),
    path('tasks/<int:task_id>/', tasks_detail, name="tasks_detail"),   #Espera parametros
    path('tasks/<int:task_id>/complete/', complete_task, name="complete_task"), #Espera parametros
    path('tasks/<int:task_id>/delete/', delete_task, name="delete_task"), #Espera parametros
] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
