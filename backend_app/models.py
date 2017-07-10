from django.db import models
import os
import shutil
import Judge.scripts.constants as const
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from collections import defaultdict
from compositefk.fields import CompositeForeignKey
from django.db.models.deletion import CASCADE
from datetime import datetime


class Question(models.Model):
	q_id = models.IntegerField(primary_key=True)
	problem_name = models.CharField(max_length=200)
	problem_statement = models.TextField()
	constraints = models.TextField()
	time_limit = models.IntegerField(default = 1)
	sample_ip = models.TextField()
	sample_op = models.TextField()

	def __str__(self):
		return str(self.q_id)

	def delete(self):
		path_to_question = os.path.join(const.PATH_TO_TESTCASE, const.Q + str(self.q_id))
		shutil.rmtree(path_to_question)
		super().delete()


def save_to_file(filepath, content):
	with open(filepath, "w") as fobj:
		fobj.write(content)

class TestCase(models.Model):
	tc_id = models.AutoField(primary_key=True)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	ip = models.TextField()
	op = models.TextField()
	score = models.IntegerField()

	def save(self):
		super().save()
		path_to_question = os.path.join(const.PATH_TO_TESTCASE, const.Q + str(self.question.q_id))
		if not os.path.isdir(path_to_question):
			os.mkdir(path_to_question)
		save_to_file(os.path.join(path_to_question, const.IP + str(self.tc_id)), self.ip)
		save_to_file(os.path.join(path_to_question, const.OP + str(self.tc_id)), self.op)

	def delete(self):
		path_to_question = os.path.join(const.PATH_TO_TESTCASE, const.Q + str(self.question.q_id))
		os.remove(os.path.join(path_to_question, const.IP + str(self.tc_id)))
		os.remove(os.path.join(path_to_question, const.OP + str(self.tc_id)))
		super().delete()

	def __str__(self):
		return str(const.Q + str(self.question.q_id) + ":"  + "tc " + str(self.tc_id))

	def get_score(self):
		self.score


class Submissions(models.Model):
	sub_id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	lang_id = models.IntegerField(
		validators=[MaxValueValidator(4), MinValueValidator(1)])
	score = models.IntegerField()
	time = models.DateTimeField(default=datetime.now)

	def __str__(self):
		return str(self.sub_id)

	@staticmethod
	def get_best_score(user, question):
		sub_obj_list = Submissions.objects.filter(user=user, question=question)
		score_list = [sub_obj.score for sub_obj in sub_obj_list]
		return max(score_list)

	@staticmethod
	def get_best_score_time(user, question):
		sub_obj_list = Submissions.objects.filter(user=user, question=question)
		best_score = 0
		time = 0
		if len(sub_obj_list) != 0:
			time = sub_obj_list[0].time
		for sub_obj in sub_obj_list:
			if sub_obj.score > best_score:
				best_score = sub_obj.score
				time = sub_obj.time
			elif sub_obj.time < time and sub_obj.score == best_score:
				time = sub_obj.time
		return time


class SubmissionResults(models.Model):
	submission = models.ForeignKey(Submissions, on_delete=models.CASCADE)
	testcase = models.ForeignKey(TestCase, on_delete=models.CASCADE)
	status = models.IntegerField(
		validators=[MaxValueValidator(4), MinValueValidator(0)] )

	class Meta:
		unique_together = [('testcase', 'submission'),] # Only one row with same tc_id and sub_id

	def __str__(self):
		return "sub_id:"+str(self.submission.sub_id)+" tc_id:"+str(self.testcase.tc_id)

	@staticmethod
	def get_score(submission, testcase):
		result_obj = SubmissionResults.objects.get(submission=submission, testcase=testcase)
		if result_obj.status != 4:
			return 0
		else:
			return testcase.get_score()