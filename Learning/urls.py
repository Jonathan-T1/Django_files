from django.urls import path
from .views import *
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.auth.decorators import login_required



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
    path('cursos/',login_required(CoursesView.as_view()), name='cursos'),
    path('crear/curso/',crear_curso,name='crear_curso'),
    path('curso/<int:pk>/edit/',login_required(CourseEditView.as_view()),name='editar_curso'),
    path('curso/<int:pk>/delete',login_required(CourseDeleteView.as_view()),name='borrar_curso'),
    path('error/',login_required(ErrorView.as_view()),name='error'),
    

#This are the task that Cesar did 
    path('tasks/', tasks, name="tasks"),
    path('tasks_completed/', tasks_completed, name="tasks_completed"),
    path('tasks/create/', create_task, name="create_task"),
    path('tasks/<int:task_id>/', tasks_detail, name="tasks_detail"),   #Espera parametros
    path('tasks/<int:task_id>/complete/', complete_task, name="complete_task"), #Espera parametros
    path('tasks/<int:task_id>/delete/', delete_task, name="delete_task"), #Espera parametros
] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
