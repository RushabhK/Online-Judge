import os, sys

PATH_TO_SCRIPT = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.dirname(PATH_TO_SCRIPT) #Path of ONLINE_JUDGE

PATH_TO_SUBMISSION = os.path.join(BASE_DIR, "submissions")
if not os.path.isdir(PATH_TO_SUBMISSION):
	os.mkdir(PATH_TO_SUBMISSION)

PATH_TO_TESTCASE = os.path.join(BASE_DIR, "testcases")
if not os.path.isdir(PATH_TO_TESTCASE):
	os.mkdir(PATH_TO_TESTCASE)

IP = "ip"
OP = "op"
Q = "q"

'''
LANGUAGE ID:
1 - C
2 - CPP
3 - JAVA
4 - PYTHON
'''

COMPILE_CMD = ["", "gcc", "g++", "javac"]
EXTENSION = ["", ".c", ".cpp", ".java", ".py"]

CODE_FILE = "Program"
COMPILE_FILE = "compile_error"
RUNTIME_FILE = "runtime_error"
RESULT_FILE = "result.json"

RUN_CMD_1 = ["", "",          "",          "java",    "python"]
RUN_CMD_2 = ["", "./Program", "./Program", "Program", "Program.py"]

MEMORY_LIMIT = "50M"
PROCESS_LIMIT = "100"
TIMEOUT = "10"

DOCKER_BASE_DIR = "/tmp"
DOCKER_SUBMISSION_PATH = os.path.join(DOCKER_BASE_DIR, "submissions")
DOCKER_TESTCASE_PATH = os.path.join(DOCKER_BASE_DIR, "testcases")
DOCKER_SCRIPT_PATH = os.path.join(DOCKER_BASE_DIR, "scripts")

'''
FLAGS:
0 - Compile time Error
1 - Runtime Error
2 - Time Limit Exceed
3 - Wrong Answer
4 - Accepted
'''
STATUS = {}
STATUS[0] = "Compile Time Error!"
STATUS[1] = "Run Time Error!"
STATUS[2] = "Time Limit Exceeded!"
STATUS[3] = "Wrong Answer!"
STATUS[4] = "Accepted!!"