from django.db import models

# Create your models here.

class User(models.Model):
    user = models.CharField(max_length=64,null=False,default='');
    username = models.CharField(max_length=32,blank=False,null=False);
    password = models.CharField(max_length=128,blank=False,null=False);
    friends = models.ManyToManyField('self');
    groups = models.ManyToManyField('UserGroup',default=100000);

    def __str__(self):
        return self.username;

class UserGroup(models.Model):
    group_name = models.CharField(max_length=32);

    def __str__(self):
        return self.group_name;

class Messages(models.Model):
    from_id = models.IntegerField();
    to_id = models.PositiveIntegerField();
    message = models.CharField(max_length=256);
    c_date = models.DateTimeField();

    def __str__(self):
        return self.message;

class testDate(models.Model):
    ctime = models.DateTimeField(auto_now_add=True);
    cdate = models.DateField(auto_now_add=True);
    name = models.CharField(max_length=32);