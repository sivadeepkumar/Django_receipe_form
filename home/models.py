from django.db import models
from django.contrib.auth.models import User 
# Create your models here.


class Receipe(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    receipe_name = models.TextField(max_length=100)
    receipe_description = models.TextField()
    receipe_image = models.ImageField()
    rating = models.IntegerField()
    price = models.IntegerField()
    count = models.IntegerField()



    def __str__(self) -> str:
        return '{},{},{}'.format(self.receipe_name,self.receipe_description,self.receipe_image)     
    


class Department(models.Model):
    department = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.department
    class Meta:
        ordering = ['department']

class StudentID(models.Model):
    student_id = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.student_id
    
class Student(models.Model):
    department = models.ForeignKey(Department,  related_name='depart',on_delete=models.CASCADE)
    student_id = models.OneToOneField(StudentID,related_name = 'studentid',on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_email =  models.EmailField(unique=True)
    student_age = models.IntegerField(default=18)
    student_address = models.TextField()


    def __str__(self) -> str:
        return self.student_name
    
    class Meta:
        ordering = ['student_name']
        verbose_name = 'student'

         