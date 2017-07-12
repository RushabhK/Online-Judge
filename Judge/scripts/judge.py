import subprocess
from constants import *
import os
import time

'''
FLAGS:
0 - Compile time Error
1 - Runtime Error
2 - Time Limit Exceed
3 - Wrong Answer
4 - Accepted
'''

def get_tc_ids(path_to_q_no):
	files_list = os.listdir(path_to_q_no)
	tc_id_list = []
	for file in files_list:
		path_to_ip_tc = os.path.join(path_to_q_no, file)
		if os.path.isfile(path_to_ip_tc):
			if file[:2] == "ip" and file[2:].isdigit() and (OP+file[2:] in files_list):
				tc_id_list.append(int(file[2:]))
	return tc_id_list

class Judge:
	def __init__(self, team_id, sub_id, lang_id, q_no, time_limit):
		try:
			self.team_id = team_id
			self.sub_id = sub_id
			self.lang_id = lang_id
			self.q_no = q_no
			self.time_limit = time_limit
			self.path_to_team = os.path.join(PATH_TO_SUBMISSION, str(team_id) )
			self.path_to_sub_id = os.path.join(self.path_to_team, str(sub_id))
			self.path_to_q_no = os.path.join(PATH_TO_TESTCASE, Q + str(q_no) )
			self.filename = CODE_FILE + EXTENSION[self.lang_id]
			self.path_to_file = os.path.join(self.path_to_sub_id, self.filename)
			self.is_valid = True
			if self.lang_id < 1 or self.lang_id > 4:
				raise ValueError("Invalid language id" + str(lang_id) )
			if time_limit < 0:
				raise ValueError("Invalid time limit value " + str(time_limit))
			if not os.path.isdir(self.path_to_team):
				raise Exception("No folder " + self.path_to_team + "exists")
			if not os.path.isdir(self.path_to_sub_id):
				raise Exception("No folder " + self.path_to_team + "exists")
			if not os.path.isdir(self.path_to_q_no):
				raise Exception("No folder " + self.path_to_q_no + "exists")
			if not os.path.isfile(self.path_to_file):
				raise Exception("File " + self.path_to_file + " doesn't exist!")
		except Exception as e:
			print (e)
			self.is_valid = False

	def check_compilation(self): #Returns True for successful compilation, else False
		if not self.is_valid:
			print ("Details not valid!")
			return
		try:
			if self.lang_id > 3:
				raise ValueError("Invalid language id for compilation!")
			path_to_compile_file = os.path.join(self.path_to_sub_id, COMPILE_FILE)
			compile_error_obj = open(path_to_compile_file, "w")
			cmd = COMPILE_CMD[self.lang_id]
			process_obj = 0
			if self.lang_id <= 2:  # For C and C++, create executable at the specified path
				path_to_exe = os.path.join(self.path_to_sub_id, CODE_FILE)
				process_obj = subprocess.Popen( [cmd, self.path_to_file, "-o", path_to_exe], 
												stderr = compile_error_obj )
			else: #For Java	
				process_obj = subprocess.Popen( [cmd, self.path_to_file], 
												stderr = compile_error_obj )
			while process_obj.poll() is None:  #Wait till the thread has not terminated
				continue
			compile_error_obj.close()
			compile_flag = process_obj.poll()  #Exit status for compilation
			if compile_flag == 0:
				print ("Compilation Successful!")
				return True
			else:
				print ("Compilation Error!")
				return False		
		except Exception as e:
			print (e)

	def check_rte_and_tle(self, tc_no): # Returns 1 for RTE, 2 for TLE, 3 for Success
		if not self.is_valid:
			print ("Details not valid!")
			return	
		path_to_ip_tc = os.path.join(self.path_to_q_no, IP + str(tc_no) )
		path_to_op = os.path.join(self.path_to_sub_id, OP + str(tc_no) )
		path_to_runtime_file = os.path.join(self.path_to_sub_id, RUNTIME_FILE + str(tc_no) )
		input_obj = open(path_to_ip_tc, "r")
		output_obj = open(path_to_op, "w")
		runtime_error_obj = open(path_to_runtime_file, "w")
		process_obj = 0
		os.chdir(self.path_to_sub_id) #Change directory to executables
		if self.lang_id <= 2: #C and C++
			process_obj = subprocess.Popen( [ RUN_CMD_2[self.lang_id] ],
											stderr = runtime_error_obj,
											stdin = input_obj,
											stdout = output_obj )
		else: #For java and python
			process_obj = subprocess.Popen( [ RUN_CMD_1[self.lang_id], RUN_CMD_2[self.lang_id] ],
											stderr = runtime_error_obj,
											stdin = input_obj,
											stdout = output_obj )
		time.sleep(self.time_limit) #Timeout for the thread
		process_status = process_obj.poll()
		runtime_error_obj.close()
		input_obj.close()
		output_obj.close()
		if process_status is None:
			print ("TLE!")
			process_obj.kill()
			return 2
		elif process_status == 0:
			print ("Ran without errors!")
			return 3
		else:
			print ("Runtime Error!")
			return 1

	def generate_result(self): #Returns a list of flags for the i/p testcases
		if not self.is_valid:
			print ("Details not valid!")
			return

		tc_id_list = get_tc_ids(self.path_to_q_no)

		result = {}
		if self.lang_id <= 3: #Language other than python
			if not self.check_compilation(): #Compile Error
				for tc_no in tc_id_list:
					result[tc_no] = 0
				return result

		for tc_no in tc_id_list:
			path_to_ip_tc = os.path.join(self.path_to_q_no, IP + str(tc_no) )
			path_to_op_tc = os.path.join(self.path_to_q_no, OP + str(tc_no) )
			path_to_my_op = os.path.join(self.path_to_sub_id, OP + str(tc_no) )
			flag = self.check_rte_and_tle(tc_no)
			if flag == 3: #Ran successfully
				my_op_obj = open(path_to_my_op, "r")
				actual_op_obj = open(path_to_op_tc, "r")
				my_op = my_op_obj.read().rstrip()
				actual_op = actual_op_obj.read().rstrip()
				my_op_obj.close()
				actual_op_obj.close()
				if my_op == actual_op: #AC
					result[tc_no] = 4
				else: #WA
					result[tc_no] = 3
			else:
				result[tc_no] = flag
		return result
