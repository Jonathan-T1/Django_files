from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse_lazy
from .forms import *
from .models import Registration
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.views.generic import DetailView,TemplateView,UpdateView,DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings
import os


# Create your views here.

def home(request):
    return render(request,'composition/home.html')

@login_required
def profile(request):
    cohorte = Cohorte.objects.all().order_by('-id')
    return render(request,'teacherandstuden/profile.html',{'cohorte':cohorte})

@login_required
def Learning(request):
    return render(request,'composition/learning.html')

def exit (request):
    logout(request)
    return redirect ('home')

@login_required
def datosus (request):
    if request.user.is_staff:
        user = User.objects.all()
        data = {
            'user': user,
        }
        return render(request,'UsersOPS/ver_user.html',data)
    else:
        return redirect('error')

@login_required    
def editaruser (request, pk):
    if request.user.is_staff:
        editarrol = get_object_or_404(User, id=pk)
        data = {
            'form': editarUser(instance=editarrol),
            'title': 'Editar Usuario'
        }
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
    else:
        return redirect('error')
@login_required
def delete_user(request, pk):
    if request.user.is_staff:
        user = get_object_or_404(User, id=pk)

        if request.method == 'POST':
            user.delete()
            return redirect('see_users')
        return render(request,'UsersOPS/delete_user.html',{'user':user})
    else:
        return redirect('error')

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
    
@login_required    
def register(request):
    if request.user.is_staff:
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
    else:
        return redirect('error')

@login_required
def crear_curso(request):
    if request.user.is_staff:
        data = {
            'form': CursoForm()
        }

        if request.method == 'POST':
            curso_creation_form = CursoForm(data=request.POST)

            if curso_creation_form.is_valid():
                curso_creation_form.save()

                return redirect('cursos')
            else:
                messages.error(request, 'Hubo un error al crear el curso. Por favor, corrige los errores.')

                data ['form'] = curso_creation_form
        return render(request,'Cohortes/crear_curso.html',data)
    else:
        return redirect('error')
@login_required
def update_profile(request):
    """Update a user's profile view."""
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            profile.biography = data ['biography']
            profile.address = data ['address']
            profile.picture = data ['picture']
            profile.save()

            return redirect('learning_overview')
        
    else:
        form = ProfileForm()
    return render(
        request=request,
        template_name='UsersOPS/update_profile.html',
        context={
            'profile': profile,
            'user': request.user,
            'form': form
        }
    )

class UserDetailView(DetailView):
    """User datail view."""
    template_name = 'teacherandstuden/profile.html'
    slug_field ='username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()

class ErrorView(TemplateView):
    template_name = 'composition/error_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        error_image_path = os.path.join(settings.MEDIA_URL,'error.jpg')
        context ['error_image_path'] = error_image_path
        return context

class CoursesView(TemplateView):
    template_name = 'Cohortes/cursos.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Cohorte.objects.all().order_by('-id')
        student = self.request.user if self.request.user.is_authenticated else None

        for item in courses:
            if student:
                registration = Registration.objects.filter(course= item,student=student).first()
                item.is_enrolled = registration is not None
            else:
                item.is_enrolled = False

            enrollment_count = Registration.objects.filter(course=item).count()
            item.enrollment_count = enrollment_count

        context['courses'] = courses
        return context
    """
    def handle_no_permission(self):
        return redirect('error_page')"""
    
class CourseEditView(UserPassesTestMixin,UpdateView):
    model = Cohorte
    form_class = CursoForm
    template_name = 'Cohortes/edit_curso.html'

    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        return redirect('error')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request,'la actualizacion del curso se ha echo satisfactoriamente')
        return redirect('cursos')
    
    def form_invalid(self, form):
        messages.error(self.request,'Ha ocurrido un error al actualizar el curso')
        return self.render_to_response(self.get_context_data(form=form))    
    
class CourseDeleteView(UserPassesTestMixin,DeleteView):
    model = Cohorte
    template_name = 'Cohortes/delete_curso.html'
    success_url = reverse_lazy("cursos")

    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        return redirect('error')
    
    def form_valid(self, form):
        messages.success(self.request,'Se ha logrado borrar al curso satisfactoriamente')
        return super().form_valid(form)