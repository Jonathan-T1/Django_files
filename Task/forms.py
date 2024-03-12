"""Task Urls"""
# Django
from django import forms

# Task Form
from .models import Task, Calificacion

class TaskForm(forms.ModelForm, ):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), label='Description')

    class Meta:
        model = Task
        fields = ['title', 'description','curso','field',]
        
    def __init__(self, *args, **kwargs):
        #este es el metodo constructor de la clase
        #init sirve para instanciar un objrto de una clase
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['field'].widget = forms.ClearableFileInput(attrs={'multiple': False})
        #el clearblefileinput permite seleccionar varios archivos

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['student','mark1','mark2','mark3','average','tareas']