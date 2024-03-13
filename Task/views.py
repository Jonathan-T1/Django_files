from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
# cuando yo ejecute esta clase UserCreationForm me va a devolver un formulario
#autentication comprobara si el usuario existe
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.generic import DetailView,TemplateView,UpdateView,DeleteView,View
#el login creara la cookie
from .forms import TaskForm, CalificacionForm
from .models import Task, Calificacion,Cohorte,Registration
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.



@login_required 
def tasks(request):
    
    tasks =Task.objects.filter( datecompleted__isnull=True)
    #devolver todas las tareas de la base de datos
    #filter(user=request.user) esto mostrara solo las tareas que correspondan al usuario que inicio sesion,no vera las tareas de otros usuarios
    #tambien mostrara las tareas que aun no estan completadas
    
    return render(request, 'Task/tasks.html',{'tasks':tasks})
#te pasare el dato al front,con el dato de tareas que se ha consultado

#render espera el parametro request
 #espera usuario y contraseña para guardarlo en ese usuario
         #devolvera un objto user

@login_required         
def tasks_completed(request):    
      tasks =Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by
      ('-datecompleted') 
      #ordena las tareas segun su fecha
      return render(request, 'Task/tasks.html',{'tasks':tasks})

@login_required
def create_task(request):
    if request.user.is_staff or request.user.is_profesor or request.user.is_Estudiante:
        courses = Cohorte.objects.all()  # Obtener todos los cursos disponibles

        if request.method == 'GET':
            return render(request, 'Task/create_task.html', {'form': TaskForm, 'courses': courses})
        else:
            try:
                form = TaskForm(request.POST, request.FILES)
                if form.is_valid():
                    new_task = form.save(commit=False)
                    new_task.user = request.user
                    new_task.save()
                    print(new_task)
                    return redirect('tasks:tasks')
            except ValueError:
                return render(request, 'Task/create_task.html', {
                    'form': TaskForm,
                    'courses': courses,  # Pasa la lista de cursos al contexto
                    'error': 'Por favor, envía datos válidos'
                })
    else:
        return redirect('error')
      
class TaskCreationView(View):
    template_name = 'Task/create_task.html'
    def get(self, request, course_id):
        course = Cohorte.objects.get(id=course_id)
        form = TaskForm()
        return render(request, 'Task/create_task.html', {'form': form, 'course': course})

    def post(self, request, course_id):
        course = Cohorte.objects.get(id=course_id)
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.course = course
            task.save()
            # Asignar la tarea a todos los estudiantes inscritos en el curso
            students = Registration.objects.filter(course=course).values_list('student', flat=True)
            for student_id in students:
                registration = Registration.objects.get(course=course, student_id=student_id)
                registration.task = task
                registration.save()
            return redirect('Cohortes/course_detail', course_id=course_id)
        return render(request, 'Task/create_task.html', {'form': form, 'course': course})

def tasks_completed2(request):  # Vista de Tareas completadas
    if request.user.is_staff or request.user.is_profesor:
        tasks = Task.objects.filter(datecompleted__isnull=False).order_by('-datecompleted')
    else:
        tasks = Task.objects.filter(curso_user=request.user, datecompleted_isnull=False).order_by('-datecompleted')
    
    return render(request, 'Task/tasks_completed.html', {
        'tasks': tasks
    })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        # Obtén la tarea y asegúrate de que pertenezca al usuario a través del modelo Cohorte
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(instance=task)
        return render(request, 'Task/task_detail.html', {'task': task, 'form': form})
    else:
        try:
            # Similarmente, asegúrate de que la tarea pertenezca al usuario a través del modelo Cohorte
            task = get_object_or_404(Task, pk=task_id)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks:tasks')
        except ValueError:
            return render(request, 'tasks:task_detail', {'task': task, 'form': form, 'error': 'Error al momento de actualizar la tarea'})

@login_required
def complete_task(request,task_id):
  task = get_object_or_404(Task, pk=task_id)
  #buscara la tarea por el primari key osea el id de la tarea
  #y solamente mostrara la tarea de ese id
  if request.method == 'POST':
      task.datecompleted = timezone.now()
      task.save()
      return redirect('tasks:tasks')
  #si es post actualizara la tarea y le mostrara la fecha
  #si tiene una fecha es porque ya se cumplio esa tarea
  #lo re direccionara a la vista de tareas
  
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:tasks')
    return redirect('Task/task_detail', task_id=task_id)

@login_required  
def calificar_tarea(request, task_id):
    tarea = Task.objects.get(id=task_id)
    
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.tarea = tarea
            calificacion.usuario = request.user
            calificacion.save()
            return redirect('task_detail', task_id=task_id)
    else:
        form = CalificacionForm()
    
    return render(request, 'Task/calificar_tarea.html', {'form': form, 'tarea': tarea})

#def calificar_tarea(request, tarea_id):
 #   tarea = Task.objects.get(pk=tarea_id)
    
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.task = tarea
            calificacion.usuario = request.user
            calificacion.save()
            return redirect('task_detail', task_id=tarea_id)  # Redirige a la vista de detalle de tarea
    else:
        form = CalificacionForm()
    
    return render(request, 'calificartarea.html', {'form': form, 'tarea': tarea})
        
def nota(request):
    notas = Calificacion.objects.filter(student=request.user)
    total_notas = notas.count()
    promedio = sum([nota.average for nota in notas]) / total_notas if total_notas > 0 else 0
    return render(request, 'Task/notas.html', {'notas': notas, 'promedio': promedio})


def create_nota(request, task_id=None):
    if request.method == 'GET':
        return render(request, 'Task/create_nota.html', {'form': CalificacionForm})
    else:
        try:
            form = CalificacionForm(request.POST, request.FILES)
            if form.is_valid():
                new_nota = form.save(commit=False)
                new_nota.user = request.user
                new_nota.save()
                return redirect('tasks:notas')
        except ValueError:
            return render(request, 'Task/create_nota.html', {
                'form': CalificacionForm,
                'error': 'Por favor, envía datos válidos'
            })

@login_required
def nota_detail(request, nota_id):
    nota = get_object_or_404(Calificacion, pk=nota_id, student=request.user)
    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            return redirect('notas')
    else:
        form = CalificacionForm(instance=nota)
    return render(request, 'Task/notas_detail.html', {'nota': nota, 'form': form})

            
def complete_nota(request,task_id):
  task =  get_object_or_404(Calificacion, pk=task_id, user=request.user )

  if request.method == 'POST':
      nota.save()
      return redirect('tasks')

  
@login_required
def delete_nota(request,task_id):
  task =  get_object_or_404(Calificacion, pk=task_id, user=request.user )
  if request.method == 'POST':
      nota.delete()
      return redirect('tasks')   
    
    
@login_required
def lista_notas(request):
    notas = Calificacion.objects.filter(student=request.user)
    return render(request, 'Task/lista_notas.html', {'notas': notas})