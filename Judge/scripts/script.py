import os
import sys
from judge import Judge
from constants import *

#team_id, sub_id, lang_id, q_no, time_limit

try:
	if len(sys.argv) != 6:
		raise ValueError("Invalid number of arguments!")
	team_id = str(sys.argv[1])
	sub_id = int(sys.argv[2])
	lang_id = int(sys.argv[3])
	q_no = int(sys.argv[4])
	time_limit = int(sys.argv[5])
	judge_obj = Judge(team_id, sub_id, lang_id, q_no, time_limit)
	result = judge_obj.generate_result()
	if result is None:
		raise Exception("Invalid result generated")
	path_to_team = os.path.join(PATH_TO_SUBMISSION, str(team_id) )
	path_to_sub_id = os.path.join(path_to_team, str(sub_id))
	path_to_result = os.path.join(path_to_sub_id, RESULT_FILE)
	result_obj = open(path_to_result, "w")
	result = [str(i) for i in result]
	s = ' '.join(result)
	result_obj.write(s)
	result_obj.close()
except Exception as e:
	print e