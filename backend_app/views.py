from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Question, TestCase, Submissions, SubmissionResults
from datetime import datetime
from Backend.settings import *

def time_in_sec(d):
	print(START_TIME)
	pass

def index(request):
	return render(request, 'backend_app/index.html', {})

@login_required
def questions(request):
	quest_list = Question.objects.all()
	d = {}
	d['questions'] = quest_list
	return render(request, 'backend_app/questions.html', d)


@login_required
def display_question(request, q_id):
	q_obj = Question.objects.get(pk=q_id)
	d = {}
	d['q_obj'] = q_obj
	return render(request, 'backend_app/display_question.html', d)

def leaderboard(request):
	return HttpResponse("This is Leaderboard")