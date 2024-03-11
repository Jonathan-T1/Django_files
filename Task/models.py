"""Task Models"""

#DJANGO
from django.db import models
from django.db.models import Q
#APP leaning
from Learning.models import User,Cohorte,Registration


class Task(models.Model):
    #aca creara la tabla
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    field = models.FileField(upload_to='archivos_adjuntos',blank=True, null=True)
    #blanck y null,permite qye estos campos puedan estar vacios en el formulario
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important= models.BooleanField(default=False)
    #si se elimina un dato de user,todo lo q tenga q ver con ese usuario se eliminara en cascada
    curso = models.ForeignKey(Cohorte,on_delete=models.CASCADE ,blank=True,null=True)
    def __str__(self):
     return f"{self.title} by {self.curso}"
   #se concardena el titulo de la tarea y el usuario que la envia



class Calificacion(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    tareas= models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    mark1 = models.PositiveIntegerField(null=True, blank=True, verbose_name='nota1')
    mark2 = models.PositiveIntegerField(null=True, blank=True, verbose_name='nota2')
    mark3 = models.PositiveIntegerField(null=True, blank=True, verbose_name='nota3')
    average = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='promedio')
    
    def __str__(self):
        return f"Calificación de {self.student.username}"

    
    #calcular rl promedio llamando a la funcion
    def calculate_average(self):
        marks = [self.mark1, self.mark2, self.mark3]
        valid_marks = [mark for mark in marks if mark is not None]
        if valid_marks:
            return sum(valid_marks) / len(valid_marks)
        return None
    
    def save(self, *args, **kwargs):
        if self.mark1 or self.mark2 or self.mark3:
            self.average = self.calculate_average()
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name ='nota'
        verbose_name_plural='notas'