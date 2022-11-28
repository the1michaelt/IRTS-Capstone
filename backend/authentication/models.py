from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.db.models import IntegerField, Model
# from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    '''
    This is a custom version of the built in User class
    It contains all of the built in fields and functionality of the standard User
    You can add fields here for any additional properties you want a User to have
    This is useful for adding roles (Customer and Employee, for example)
    For just a few roles, adding boolean fields is advised
    '''
    # Example (note import of models above that is commented out)
    # this will add a column to the user table
    is_student = models.BooleanField('Is student', default=False)

    #Below pertains only to student 
    semester = models.IntegerField(blank=True, null=True)
    gpa = models.FloatField(blank=True, null=True)
    credits_earned = models.IntegerField(blank=True, null=True) 
    grad_ready = models.BooleanField('Graduation ready', default=False)
   
    
