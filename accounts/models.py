from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    name=models.CharField(max_length=20,null=True,blank=True)
    surname=models.CharField(max_length=20,null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)