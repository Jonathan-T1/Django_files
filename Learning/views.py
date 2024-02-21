from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .forms import *
from django.utils import timezone
from django.contrib.auth import authenticate, login

# Create your views here.

def home(request):
    return render(request,'composition/home.html')

@login_required
def update_profile(request):
    """Update a user's profile view."""
    data = {
        'form': ProfileForm()
    }

    if request.method == 'POST':
        user_creation_form = ProfileForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()
            
            # Mensaje de éxito
            messages.success(request, 'Registro exitoso. ¡Ahora puedes iniciar sesión!')

            return redirect('see_users')
        else:
            # Mensaje de error
            messages.error(request, 'Hubo un error en el formulario. Por favor, corrige los errores.')

            data['form'] = user_creation_form

    return render(request, 'UsersOPS/update_profile.html', data)


@login_required
def Learning(request):
    return render(request,'composition/learning.html')
def exit (request):
    logout(request)
    return redirect ('home')

def register(request):
    data = {
        'form': CustumUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustumUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()
            
            # Mensaje de éxito
            messages.success(request, 'Registro exitoso. ¡Ahora puedes iniciar sesión!')

            return redirect('see_users')
        else:
            # Mensaje de error
            messages.error(request, 'Hubo un error en el formulario. Por favor, corrige los errores.')

            data['form'] = user_creation_form

    return render(request, 'UsersOPS/register.html', data)

def datosus (request):
    user = User.objects.all()
    data = {
        'user': user,
    }
    return render(request,'UsersOPS/ver_user.html',data)

def editaruser (request, pk):

    data = {
        'form': editarUser(),
        'title' : 'Editar Rol Usuarios'
    }
    editarrol = User.objects.get(id=pk)
    if request.method == 'POST':
        formeditus = editarUser(data=request.POST, instance=editarrol)
        if formeditus.is_valid():
            formeditus.save()

            messages.success(request, 'Se Edito el Usuario Satisfactoriamente!')

            return redirect('see_users') 
        else:
            # Mensaje de error
            messages.error(request, 'Hubo un error en el formulario. Por favor, corrige los errores.')

            data['form'] = formeditus           

    return render(request, 'UsersOPS/editaruser.html', data)

def delete_user(request, pk):
    user = get_object_or_404(User, id=pk)

    if request.method == 'POST':
        user.delete()
        return redirect('see_users')
    return render(request,'UsersOPS/delete_user.html',{'user':user})

def Cambiar_contraseña(request,pk):
    data={
        'form':ChangePasswordForm(),
        'title' : 'Editar Usuario'
    }
    usuario = User.objects.get(id=pk)
    if request.method == 'POST':
        user_Change_password = ChangePasswordForm(data=request.POST, instance=usuario)

        if user_Change_password.is_valid():
            user_Change_password.save()
            messages.success(request, "Contraseña Editada Con Éxito")
            return redirect('home')
        else:
            messages.error(request, "Error al Editar Contraseña")
    return render(request, 'UsersOPS/change_password.html', data)

def tasks(request): #Vista de tareas
    # tasks = Task.objects.all() #Para mostrar todos los usurios SIRVE PARA VISTA DOCENTE
    # Muestra las tareas del un usuario en espeficico y solo las que a un estan por completar
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'homeworks/tasks.html', {
        'tasks': tasks
    })

def tasks_completed(request): #Vista de Tareas completadas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'homeworks/tasks.html', {
        'tasks': tasks
    })

def create_task(request): #Crear tarea
    if request.method == 'GET':
        return render(request, 'homeworks/create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'homeworks/create_task.html', {
                'form': TaskForm,
                'error': 'Please provide valida data'
            })
        
def tasks_detail(request, task_id): #Actualizar tareas
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)#Busca por el id de la tarea y el usuario debe ser igual 
        form = TaskForm(instance=task)
        return render(request, 'homeworks/tasks_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:          
            tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
            task = get_object_or_404(Task, pk=task_id,  user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            title = Task.objects.get(pk=task_id).title
            return render(request, 'homeworks/tasks.html', {
                'msg': 'Actualizacion: ', 
                'title':title,
                'tasks': tasks

            })
        except ValueError:
            task = get_object_or_404(Task, pk=task_id)
            form = TaskForm(instance=task)
            return render(request, 'homeworks/tasks_detail.html', {
                'error': 'Error updatign task',
                'form': form
            })

def complete_task(request, task_id): #Completar Tarea
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect ('tasks')
    
def delete_task(request, task_id): #Eliminar Tarea
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect ('tasks')
    
def cohorte(request):
    cohorte = Cohorte.objects.all()
    return render(request,'Cohortes/cohortes.html',{'cohorte':cohorte})


