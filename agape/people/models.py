from django.db import models

# Create your models here.
class Person (models.Model):

    entity = 'person'

    FEMALE = 'f'
    MALE = 'm'
    GENDER_CHOICES = (
        ("", '-- select --'),
        (FEMALE, 'Female'),
        (MALE, 'Male')
    )
    
    progenitor  = models.CharField(max_length=64,null=True,blank=True)
    title       = models.CharField(max_length=16,null=True,blank=True)

    first_name  = models.CharField(max_length=32,null=False,blank=False)
    middle_name = models.CharField(max_length=32,null=True ,blank=True)
    last_name   = models.CharField(max_length=32,null=True ,blank=True)
    
    gender      = models.CharField(max_length=1,null=True,blank=True,choices=GENDER_CHOICES)
    birthday    = models.DateField(blank=True,null=True)

    def moniker(self):
        return '{}:{}'.format(self.entity, self.id)

    def __str__(self):
        return '<{} {} {}>'.format(self.moniker(), self.first_name, self.last_name)
