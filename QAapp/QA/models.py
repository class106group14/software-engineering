from django.db import models

# Create your models here.
class Answer(models.Model):
    answer = models.CharField(primary_key=True,max_length = 220)
    score = models.FloatField()
    
    def __unicode__(self):
        return self.answer

class Question(models.Model):
    question = models.CharField(primary_key=True,max_length = 100)
    answers = models.ManyToManyField(Answer)
    def __unicode__(self):
        return self.question
        
class Questionans(models.Model):
    question = models.CharField(primary_key=True,max_length = 100)
    answers = models.ManyToManyField(Answer)
    def __unicode__(self):
        return self.question

class User(models.Model):
    username = models.CharField(primary_key=True,max_length = 30)
    password = models.CharField(max_length = 50)
    myquestions = models.ManyToManyField(Question)#not same class yiyong
    myanswers = models.ManyToManyField(Questionans)
    limit = models.NullBooleanField()
    
    def __unicode__(self):
        return self.username

#class Manager(models.Model):##
 #   ID = models.CharField(max_length = 20)
  #  password = models.CharField(max_length = 50)
