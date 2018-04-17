import sys

class Bank:
	def __init__(self, num_chickens, num_wolves, has_boat):
		self.num_chickens = num_chickens
		self.num_wolves = num_wolves
		self.has_boat = has_boat


class State:
	def __init__(self, left_bank, right_bank):
		self.left_bank = left_bank
		self.right_bank = right_bank

	def __str__(self):
		return "%s, %s, %s\n%s, %s, %s\n" % (self.left_bank.num_chickens,
											 self.left_bank.num_wolves,
											 1 if self.left_bank.has_boat else 0,
											 self.right_bank.num_chickens,
											 self.right_bank.num_wolves,
											 1 if self.right_bank.has_boat else 0)

	def is_valid(self):
		return self.left_bank.num_chickens >= 0 and self.left_bank.num_wolves >= 0 and (self.left_bank.num_chickens >= self.left_bank.num_wolves or self.left_bank.num_chickens == 0) and self.right_bank.num_chickens >= 0 and self.right_bank.num_wolves >= 0 and (self.right_bank.num_chickens >= self.right_bank.num_wolves or self.right_bank.num_chickens == 0)

	def compare(self, other_state):
		return self.left_bank.num_chickens == other_state.left_bank.num_chickens and self.left_bank.num_wolves == other_state.left_bank.num_wolves and self.left_bank.has_boat == other_state.left_bank.has_boat and self.right_bank.num_chickens == other_state.right_bank.num_chickens and self.right_bank.num_wolves == other_state.right_bank.num_wolves and self.right_bank.has_boat == other_state.right_bank.has_boat


def read_state_file(filename):
	state_file = map(lambda l: l.split(","), open(filename, "r").read().split("\n"))
	return State(left_bank = Bank(num_chickens = int(state_file[0][0]),
								  num_wolves = int(state_file[0][1]),
								  has_boat = state_file[0][2] == "1"),
				 right_bank = Bank(num_chickens = int(state_file[1][0]),
								   num_wolves = int(state_file[1][1]),
								   has_boat = state_file[1][2] == "1"))


def new_successor(current_state, chickens, wolves):
	if current_state.left_bank.has_boat:
		return State(left_bank =  Bank(current_state.left_bank.num_chickens - chickens,
									   current_state.left_bank.num_wolves - wolves,
									   has_boat = False),
					 right_bank = Bank(current_state.right_bank.num_chickens + chickens,
									   current_state.right_bank.num_wolves + wolves,
									   has_boat = True))
	elif current_state.right_bank.has_boat:
		return State(left_bank =  Bank(current_state.left_bank.num_chickens + chickens,
									   current_state.left_bank.num_wolves + wolves,
									   has_boat = True),
					 right_bank = Bank(current_state.right_bank.num_chickens - chickens,
									   current_state.right_bank.num_wolves - wolves,
									   has_boat = False))


def generate_successors(current_state):
	successors = list()	
	# Put one chicken in the boat
	s = new_successor(current_state, chickens = 1, wolves = 0)
	if s.is_valid():
		successors.append(s)

	# Put two chickens in the boat
	s = new_successor(current_state, chickens = 2, wolves = 0)
	if s.is_valid():
		successors.append(s)

	# Put one wolf in the boat
	s = new_successor(current_state, chickens = 0, wolves = 1)
	if s.is_valid():
		successors.append(s)

	# Put one wolf and one chicken in the boat
	s = new_successor(current_state, chickens = 1, wolves = 1)
	if s.is_valid():
		successors.append(s)

	# Put two wolves in the boat
	s = new_successor(current_state, chickens = 0, wolves = 2)
	if s.is_valid():
		successors.append(s)

	return successors


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
