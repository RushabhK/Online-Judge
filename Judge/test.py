from scripts.judge import *

judge_obj = Judge("team1", 1, 2, 1, 1)
assert(judge_obj.check_compilation() == True)
assert(judge_obj.generate_result() == {1:4, 2:4})

judge_obj = Judge("no_such_team_exists", 1, 2, 1, 1)
assert(judge_obj.generate_result() is None)

print "Tests ran successfully!"