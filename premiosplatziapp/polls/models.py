from django.db import models
from django.utils import timezone
import datetime

class Question(models.Model):
    #id django lo crea automaticamente y de manera incremental
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    #funcion que retornara el texto del objeto
    def __str__(self):
        return self.question_text

    #funcion que permite ver si una pregunta tiene una fecha reciente de publicacion
    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


