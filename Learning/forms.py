from django import forms
from .models import User , Task ,Cohorte, Profile,Signature
from django.contrib.auth.forms import UserCreationForm


class CustumUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','cedula','phone','username','password1', 'password2','is_staff','is_profesor','is_Estudiante']
        labels = {
            'first_name': 'Nombre',
            'last_name':'Apellidos',
            'cedula':'Cedula',
            'phone': 'Phone',
            'username': 'Nombre De Usuario',
            'password1':'Contraseña',
            'password2':'Repetir Contraseña',
            'is_staff': 'is Admin ?',
            'is_profesor': 'is a Teacher ?',
            'is_Estudiante': 'is a Student ?',
        }
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Indroduzca sus Nombres'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Indroduzca sus Apellidos'}),
            'cedula':forms.TextInput(attrs={'class':'form-control','placeholder':'Indroduzca su Cedula'}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su Numero'}),
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Indroduzca su Nombre de Usuario'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Indroduzca su Contraseña'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Repita su Contraseña'}),
            'is_staff':forms.CheckboxInput(),
            'is_profesor':forms.CheckboxInput(),
            'is_Estudiante':forms.CheckboxInput(),
        }

class editarUser (forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','email','cedula','phone','is_staff','is_profesor','is_Estudiante']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
            #Modificar datos del form
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Write a title'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Write a description'}),
            'important':forms.CheckboxInput(attrs={'class':'form-check-input m-auto'})
        }

class ChangePasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1','password2']

class cohorte(forms.ModelForm):
    class Meta:
        model = Cohorte
        fields = ['codigoCoh','nombreCoh','descrptionCoh','user']

class ProfileForm(forms.Form):
    """Profile form."""
    biography = forms.CharField(max_length=500, required=False)
    picture = forms.ImageField()
    class Meta:
        model = Signature
        fields =['signature']