from django.db import models

# Create your models here.
class Answer(models.Model):
    answer = models.CharField(primary_key=True,max_length = 200)
    score = models.FloatField()

class Question(models.Model):
    question = models.CharField(primary_key=True,max_length = 200)
    answers = models.ManyToManyField(Answer)

class User(models.Model):
    username = models.CharField(primary_key=True,max_length = 30)
    password = models.CharField(max_length = 50)
    myquestions = models.ManyToManyField(Question)
    myanswers = models.ManyToManyField(Question)
    limit = models.BooleanField()

#class Manager(models.Model):##
 #   ID = models.CharField(max_length = 20)
  #  password = models.CharField(max_length = 50)
