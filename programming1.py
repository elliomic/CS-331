#!/usr/bin/python
import sys
from collections import deque

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


class Node:
	def __init__(self, state, parent):
		self.state = state
		self.parent = parent


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


def solution(node):
	path = deque()
	while node != None:
		path.appendleft(node.state)
		node = node.parent
	return path


def breadth_first_search(initial_state, goal_state):
	node = Node(initial_state, None)
	if initial_state.compare(goal_state):
		return solution(node)
	frontier = deque()
	frontier.append(node)
	explored = set()
	while frontier:
		node = frontier.popleft()
		explored.add(node.state)
		for successor in generate_successors(node.state):
			child = Node(successor, node)
			if child.state not in explored and child.state not in frontier:
				if child.state.compare(goal_state):
					return solution(child)
				frontier.append(child)
	return solution(None)


def depth_first_search(initial_state, goal_state):
	pass


def recursive_dls(node, goal_state, limit):
	if node.state.compare(goal_state):
		return solution(node)
	elif limit == 0:
		return solution(None)
	else:
		for successor in generate_successors(node.state):
			child = Node(successor, node)
			result = recursive_dls(child, goal_state, limit - 1)
			if result:
				return result
		return solution(None)


def depth_limited_search(initial_state, goal_state, limit):
	return recursive_dls(Node(initial_state, None), goal_state, limit);


def iterative_deepening_depth_first_search(initial_state, goal_state):
	for depth in xrange(0, 200):
		result = depth_limited_search(initial_state, goal_state, depth)
		if result:
			return result
	return solution(None)


def a_star_search(initial_state, goal_state):
	pass


"""<initial state file> <goal state file> <mode> <output file>"""
def main():
	mode = sys.argv[3]
	initial_state = read_state_file(sys.argv[1])
	goal_state = read_state_file(sys.argv[2])

	if mode == "bfs":
		solution_path = breadth_first_search(initial_state, goal_state)
	elif mode == "dfs":
		solution_path = depth_first_search(initial_state, goal_state)
	elif mode == "iddfs":
		solution_path = iterative_deepening_depth_first_search(initial_state, goal_state)
	elif mode == "astar":
		solution_path = a_star_search(initial_state, goal_state)
	else:
		print "Invalid mode: " + mode
		return

	if len(sys.argv) > 4:
		output = open(sys.argv[4], "w")
	else:
		output = sys.stdout
	for state in solution_path:
		output.write(str(state) + "\n")

if __name__ == "__main__":
	main()
