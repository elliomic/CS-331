import sys

class Bank:
	def __init__(self, chickens, wolves, boat):
		self.chickens = chickens
		self.wolves = wolves
		self.boat = boat


class State:
	def __init__(self, left, right):
		self.left = left
		self.right = right


def read_state_file(filename):
	state_file = map(lambda l: l.split(","), open(filename, "r").read().split("\n"))
	return State(
		Bank(int(state_file[0][0]), int(state_file[0][1]), state_file[0][2] == "1"),
		Bank(int(state_file[1][0]), int(state_file[1][1]), state_file[1][2] == "1"))


def breadth_first_search(initial_state, goal_state):
	pass


def depth_first_search(initial_state, goal_state):
	pass


def iterative_deepening_depth_first_search(initial_state, goal_state):
	pass


def a_star_search(initial_state, goal_state):
	pass


"""< initial state file > < goal state file > < mode > < output file >"""
def main():
	mode = sys.argv[3]
	initial_state = read_state_file(sys.argv[1])
	goal_state = read_state_file(sys.argv[2])

	if mode == "bfs":
		breadth_first_search(initial_state, goal_state)
	elif mode == "dfs":
		depth_first_search(initial_state, goal_state)
	elif mode == "iddfs":
		iterative_deepening_depth_first_search(initial_state, goal_state)
	elif mode == "astar":
		a_star_search(initial_state, goal_state)


if __name__ == "__main__":
	main()
