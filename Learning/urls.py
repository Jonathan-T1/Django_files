from django.urls import path,include
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
    path('staff/overview/',profile,name='staff_overview'),
    path('learning/overview/', login_required(ProfileView.as_view()), name='learning_overview'),
    path('cohorte/<int:cohorte_id>/estudiantes/', estudiantes_inscritos, name='estudiantes_inscritos'),

#This are the Curses urls
    path('cursos/',login_required(CoursesView.as_view()), name='cursos'),
    path('crear/curso/',crear_curso,name='crear_curso'),
    path('curso/<int:pk>/edit/',login_required(CourseEditView.as_view()),name='editar_curso'),
    path('curso/<int:pk>/delete',login_required(CourseDeleteView.as_view()),name='borrar_curso'),
    path('error/',login_required(ErrorView.as_view()),name='error'),
    path('enroll_course/<int:course_id>/', CourseEnrollmentView.as_view(), name='enroll_course'),
    
    

#This include all the Urls of the app Task 
    path('tasks/',include(('Task.urls','Task'),namespace='tasks')),

    
#urls donde le profesor mirara los estudiantes inscritos a su curso
    path('cohorte/<int:cohorte_id>/estudiantes/', estudiantes_inscritos, name='estudiantes_inscritos'),

] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
