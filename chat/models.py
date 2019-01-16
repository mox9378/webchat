from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=32,blank=False,null=False);
    password = models.CharField(max_length=128,blank=False,null=False);
    friends = models.ManyToManyField('self');
    groups = models.ManyToManyField('UserGroup');

    def __str__(self):
        return self.username;

class UserGroup(models.Model):
    group_name = models.CharField(max_length=32);

    def __str__(self):
        return self.group_name;