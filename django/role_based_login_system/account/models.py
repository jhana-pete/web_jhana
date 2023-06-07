from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


# Create your models here.


class User(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_student = models.BooleanField('Is student', default=False)
    is_employee = models.BooleanField('Is employee', default=False)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    title = models.CharField(max_length=100)
    email = models.EmailField()
    status = models.CharField(max_length=30, choices=(
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ))
    submitted_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    description = models.TextField()
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.title