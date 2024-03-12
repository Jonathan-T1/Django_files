from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, AbstractBaseUser,PermissionsMixin,User


class User(AbstractUser,AbstractBaseUser,PermissionsMixin):
    cedula = models.CharField(max_length=11,unique=True, verbose_name='Cedula',blank=True, help_text=(
        "Obligatorio. Digite su nemero de Cedula completo. Unicamente numeros. Sin puntos ni comas"
    ))
    phone = models.CharField(max_length=10, verbose_name='Celuar', blank=False, help_text=(
        "Obligatorio. Digite su nemero de Celular completo. Unicamente numeros. Sin puntos ni comas"
    ))
    is_profesor = models.BooleanField(
        ("Rol Profesor"),
        default=False
    )
    is_Estudiante = models.BooleanField(
        ("Estudiante"),
        default=False
    )

class Cohorte(models.Model):
    STATUS_CHOICES = (
        ('I', 'Inscripciónes Abiertas'),
        ('P', 'En Progreso'),
        ('F', 'Finalizado'),
    )
    nombreCoh = models.CharField(max_length=100)
    descrptionCoh = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    delted = models.DateTimeField(null=True,blank=True)
    teacher  = models.ForeignKey(User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to=Q(is_profesor=True)
        )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='I', verbose_name='Estado')
    def codCoh(self):
        return "{} ".format(self.nombreCoh)
    
    def __str__(self):
        return self.codCoh()

class Registration(models.Model):
    course = models.ForeignKey(Cohorte, 
        on_delete=models.CASCADE,
        verbose_name='Curso'
        )
    student = models.ForeignKey(User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='students_registration',
        limit_choices_to=Q(is_Estudiante=True),
        verbose_name='Estudiante'
        )
    def __str__(self):
        return f'{self.student.username} - {self.course.nombreCoh}'
    class Meta:
        verbose_name = 'Inscripcion'
        verbose_name_plural = 'Inscripciones'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    picture = models.ImageField(
        upload_to='users/pictures',
        blank=True,
        null=True
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return username."""
        return self.user.username










"""
class Cursos(models.Model):
    nombre = models.CharField(max_length=100)
    description = models.TextField(blank=True,max_length=500)
    students = models.ForeignKey(User, on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to=Q(is_Estudiante=True)
        )
    lecciones = models.ForeignKey(Cohorte,on_delete=models.CASCADE,null= True,blank=True)
"""
