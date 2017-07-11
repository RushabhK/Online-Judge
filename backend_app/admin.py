from django.contrib import admin
from .models import Question
from .models import TestCase
from .models import Submissions
from .models import SubmissionResults

class QuestionAdmin(admin.ModelAdmin):
	list_display = ['q_id', 'problem_name']

class TestCaseAdmin(admin.ModelAdmin):
	list_display = ['question', 'tc_id', 'ip', 'op', 'score']

class SubmissionsAdmin(admin.ModelAdmin):
	list_display = ['sub_id', 'user', 'question', 'lang_id', 'score', 'time']

class SubmissionResultsAdmin(admin.ModelAdmin):
	list_display = ['submission', 'testcase', 'status']

admin.site.register(Question, QuestionAdmin)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(Submissions, SubmissionsAdmin)
admin.site.register(SubmissionResults, SubmissionResultsAdmin)