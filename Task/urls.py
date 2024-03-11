"""Task Urls."""

# Django

from django.urls import path

# Views
from Task.views import TaskCreationView
from Task import views

urlpatterns = [
    path(route='',
         view=views.tasks, 
         name='tasks'
         ),

    path(route='tasks_completed/',
         view=views.tasks_completed, 
         name='task_completed'
         ),

     path(route='create/',
         view=views.create_task,
         name='create_task'
         ),

    path(route='create/<int:course_id>/',
         view=TaskCreationView.as_view(),
         name='create_task_with_course'
         ),

    #<int:task_id>: significa que es un dato id entero,y se enviara al task_detail
    path(route='calificar_tarea/',
         view=views.calificar_tarea, 
         name='calificar_tarea'
         ),

    path(route='create_nota/',
         view=views.create_nota,
         name='create_nota'
         ),

    path(route='nota/',
         view=views.nota, 
         name='notas'
         ),

    path(route='lista/notas/',
         view=views.lista_notas, 
         name='notas'
         ),

    path(route='<int:task_id>/nota_detail/',
         view=views.nota_detail, 
         name='nota_detail'
         ),

    path(route='<int:task_id>/complete/',
         view=views.complete_task,
         name='complete_task'
         ),

    path(route='<int:task_id>/delete/',
         view=views.delete_task,
         name='delete_task'
         ), 

    path(route='<int:task_id>/',
         view=views.task_detail,
         name='task_detail'
         ),

    path(route='notas/<int:nota_id>/',
         view=views.nota_detail, 
         name='nota_detail'
         ),

    path(route='notas/<int:nota_id>/complete/',
         view=views.complete_nota, 
         name='complete_nota'
         ),

    path(route='notas/<int:nota_id>/delete/',
         view=views.delete_nota, 
         name='delete_nota'
         ),
     path(route='complete/',
          view=views.tasks_completed2,
          name='task_completed'),
]
