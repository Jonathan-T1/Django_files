from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser,PermissionsMixin


class User(AbstractUser,AbstractBaseUser,PermissionsMixin):
    cedula = models.CharField(max_length=11,unique=True, verbose_name='Cedula', blank=False, help_text=(
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

class Task(models.Model):
    title = models.CharField(max_length=100)
    # Por defecto campo basio si no se escribe nada
    description = models.TextField(blank=True)
    # Crea por defecto la fecha en que se creo
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)  # Campo basio inicialmente
    # Por defecto no todas son importantes
    important = models.BooleanField(default=False)
    # Relaciona el FK del User
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title+" - usuario: "+self.user.username
    

class Cohorte(models.Model):
    codigoCoh = models.CharField(max_length=50,unique=True)
    nombreCoh = models.CharField(max_length=100)
    descrptionCoh = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    delted = models.DateTimeField(null=True,blank=True)
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

class Signature(models.Model):
    nameSignature = models.CharField(max_length=60)

    def signature(self):
        return "{} ".format(self.nameSignature)
    
    def __str__(self) :
        return self.signature()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(blank=True)
    signature = models.ForeignKey(Signature, on_delete=models.CASCADE)

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