from scripts.constants import *

#team_id, sub_id, lang_id, q_no, time_limit

def get_cmd(team_id, sub_id, lang_id, q_no, time_limit):
	cmd =   "docker run" + \
			" --memory-reservation " + MEMORY_LIMIT + \
			" --ulimit nproc=" + PROCESS_LIMIT + \
			" -v " + PATH_TO_SCRIPT + ":" + DOCKER_SCRIPT_PATH + \
			" -v " + PATH_TO_TESTCASE + ":" + DOCKER_TESTCASE_PATH + \
			" -v " + PATH_TO_SUBMISSION + ":" + DOCKER_SUBMISSION_PATH + \
			" -t judge_image timeout " + TIMEOUT + \
			" python " + DOCKER_SCRIPT_PATH + "/script.py " + \
															str(team_id) + " " + \
															str(sub_id) + " " + \
															str(lang_id) + " " + \
															str(q_no) + " " + \
															str(time_limit)
	return cmd

print get_cmd("team1", 1, 2, 1, 1)