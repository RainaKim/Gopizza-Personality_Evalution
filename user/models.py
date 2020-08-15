from django.db import models

from eval.models import Question, Section

class User(models.Model):
    name        = models.CharField(max_length = 50)
    password    = models.CharField(max_length = 200,null = True)
    email       = models.EmailField(max_length = 200,unique = True, blank = False)
    department  = models.ForeignKey('Department', on_delete = models.SET_NULL, null = True)
    is_active   = models.BooleanField(default=False)
    question    = models.ManyToManyField('eval.Question',through='UserQuestion')
    auth        = models.ForeignKey('Auth', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'users'

class Department(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'departments'

class UserQuestion(models.Model):
    user        = models.ForeignKey('User',on_delete = models.SET_NULL, null = True)
    question    = models.ForeignKey('eval.Question', on_delete = models.SET_NULL, null = True)
    point       = models.IntegerField(null = True)
    
    class Meta:
        db_table = 'user_questions'

class Auth(models.Model):
    name        = models.CharField(max_length = 50)

    class Meta:
        db_table = 'auths'

