from django.db import models
import os
import shutil
import Judge.scripts.constants as const

def save_to_file(filepath, content):
	with open(filepath, "w") as fobj:
		fobj.write(content)


class Question(models.Model):
	q_id = models.IntegerField(primary_key=True)
	problem_statement = models.TextField()
	constraints = models.TextField()
	time_limit = models.IntegerField(default = 1)
	sample_ip = models.TextField()
	sample_op = models.TextField()
	ip1 = models.TextField()
	op1 = models.TextField()
	score1 = models.IntegerField()
	ip2 = models.TextField()
	op2 = models.TextField()
	score2 = models.IntegerField()
	ip3 = models.TextField()
	op3 = models.TextField()
	score3 = models.IntegerField()

	def save(self):
		super().save()

		path_to_question = os.path.join(const.PATH_TO_TESTCASE, const.Q + str(self.q_id))
		if not os.path.isdir(path_to_question):
			os.mkdir(path_to_question)
		save_to_file(os.path.join(path_to_question, const.IP + "1"), self.ip1)
		save_to_file(os.path.join(path_to_question, const.IP + "2"), self.ip2)
		save_to_file(os.path.join(path_to_question, const.IP + "3"), self.ip3)
		save_to_file(os.path.join(path_to_question, const.OP + "1"), self.op1)
		save_to_file(os.path.join(path_to_question, const.OP + "2"), self.op2)
		save_to_file(os.path.join(path_to_question, const.OP + "3"), self.op3)

	def delete(self):
		super().delete()
		path_to_question = os.path.join(const.PATH_TO_TESTCASE, const.Q + str(self.q_id))
		shutil.rmtree(path_to_question)

