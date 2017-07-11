from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Question, TestCase, Submissions, SubmissionResults
from datetime import datetime
from Backend.settings import *
import Judge.scripts.constants as const
import subprocess
import json


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


def get_cmd(team_id, sub_id, lang_id, q_obj):
	cmd1 = "python"
	cmd2 = const.PATH_TO_SCRIPT + "/script.py"
	cmd3 = str(team_id)
	cmd4 = str(sub_id)
	cmd5 = str(lang_id)
	cmd6 = str(q_obj.q_id)
	cmd7 = str(q_obj.time_limit)
	cmd = [cmd1, cmd2, cmd3, cmd4, cmd5, cmd6, cmd7]
	return cmd	

def generate_program_file(team_id, lang_id, file_content, sub_id):
	if not os.path.isdir(const.PATH_TO_SUBMISSION):
		os.mkdir(const.PATH_TO_SUBMISSION)
	path_to_team = os.path.join(const.PATH_TO_SUBMISSION, str(team_id) )
	if not os.path.isdir(path_to_team):
		os.mkdir(path_to_team)

	path_to_sub_id = os.path.join(path_to_team, str(sub_id) )
	if not os.path.isdir(path_to_sub_id):
		os.mkdir(path_to_sub_id)

	filename = const.CODE_FILE + const.EXTENSION[int(lang_id)]
	path_to_file = os.path.join(path_to_sub_id, filename)
	with open(path_to_file, 'w') as w_obj:
		w_obj.write(file_content)


@login_required
def display_question(request, q_id):
	q_obj = Question.objects.get(pk=q_id)
	d = {}
	d['q_obj'] = q_obj
	if request.method == "GET":
		return render(request, 'backend_app/display_question.html', d)
	if request.method == "POST": #When user submits a solution
		is_file_present = request.FILES.get('code_file', False)
		if request.POST['lang_id'] == "" or not is_file_present: # Check for empty fields
			return HttpResponseRedirect('/questions/q'+str(q_id))
		else:
			team_id = request.user.username
			lang_id = request.POST['lang_id']
			file_content = (request.FILES['code_file'].read()).decode("utf-8")
			sub_obj = Submissions(user=request.user, question=q_obj, lang_id=lang_id, score=0)
			sub_obj.save()
			sub_id = sub_obj.sub_id
			generate_program_file(team_id, lang_id, file_content, sub_id)
			cmd = get_cmd(team_id, sub_id, lang_id, q_obj)	
			process_obj = subprocess.Popen(cmd)
			while process_obj.poll() is None:  #Wait till the thread has not terminated
				continue

			path_to_team = os.path.join(const.PATH_TO_SUBMISSION, str(team_id) )
			path_to_sub_id = os.path.join(path_to_team, str(sub_id) )
			path_to_results = os.path.join(path_to_sub_id, const.RESULT_FILE)

			if not os.path.isfile(path_to_results):
				print("HEreeee")
				return HttpResponseRedirect('/questions/q'+str(q_id))
			json_data = open(path_to_results).read()
			results = json.loads(json_data)
			print("Resultssssssssssssssss: ", results)

			d = {}
			score_details = []
			total_score = 0
			your_score = 0
			index = 1
			for tc_id, status in results.items():
				tc_obj = TestCase.objects.get(pk=int(tc_id))
				result_obj = SubmissionResults(submission=sub_obj, testcase=tc_obj, status=status)
				result_obj.save()
				score_details.append([index, result_obj.get_score(), tc_obj.score, const.STATUS[status]])
				your_score += result_obj.get_score()
				total_score += tc_obj.score
				index += 1
			d['score_details'] = score_details
			d['total_score'] = total_score
			d['your_score'] = your_score

			sub_obj = Submissions.objects.filter(pk=sub_id)
			sub_obj.update(score=total_score)
			print(total_score)
			print(score_details)

			return render(request, 'backend_app/show_result.html', d)
		

def leaderboard(request):
	return HttpResponse("This is Leaderboard")