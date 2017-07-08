from django.contrib import admin
from .models import Question

class QuestionAdmin(admin.ModelAdmin):
	list_display = ['q_id', 'problem_statement']

admin.site.register(Question, QuestionAdmin)