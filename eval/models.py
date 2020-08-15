from django.db import models

class Section(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'sections'

class Question(models.Model):
    content = models.TextField()
    section = models.ForeignKey(Section, on_delete = models.SET_NULL, null = True)
    
    class Meta:
        db_table = 'questions'

class Introduction(models.Model):
    content   = models.TextField()

    class Meta:
        db_table = 'introductions'

class Notice(models.Model):
    content = models.TextField()

    class Meta:
        db_table = 'notices'


