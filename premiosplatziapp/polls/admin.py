from secrets import choice
from django.contrib import admin
from .models import Question, Choice


#creamos la clase de Choice
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3
class QuestionAdmin(admin.ModelAdmin):
    #nos ayuda a colocar el orden del administrador 
    fields = ["pub_date", "question_text"]
    #colocamos la clase de respuestas a las preguntas
    inlines = [ChoiceInline]
    #puede colocar los datos que se mostraran
    list_display= ("question_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)
