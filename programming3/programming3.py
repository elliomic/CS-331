#!/usr/bin/python
"""
CS 331 Assignment #3: Sentiment Analysis
Anish Asrani, Michael Elliott
"""
import sys, string
import pprint
import itertools as it
import collections

def file_len(fname):
    with open(fname, "r") as f:
		return sum(1 for line in f)

def classify_data(infile, outfile):
	vocab = dict()
	train = collections.defaultdict(list)
	classlabel = []

	num_lines = file_len(infile)
	with open(infile, "r") as input_file:
		current_line = 0
		for line in input_file:
			line = line.split()
			classlabel.append(line[-1])

			for word in line[:-1]:
				word = word.lower().translate(None, string.punctuation+string.digits)
				if word == "":
					continue

				try:
					vocab[word][current_line] = 1
				except:
					vocab[word] = [0 for i in xrange(num_lines)]
					vocab[word][current_line] = 1
			current_line += 1

	current_file = open(outfile, 'w')
	pp = pprint.PrettyPrinter(indent = 4, stream = current_file)
	pp.pprint(vocab)

	for key in vocab:
		neg_count = 0
		pos_count = 0
		for i in range(0, len(classlabel)):
			if vocab[key][i] == 1: 
				if classlabel[i] == '1':
					pos_count += 1
				elif classlabel[i] == '0':
					neg_count += 1
		train[key].append((pos_count, neg_count))
	print(train)


def main(): 
	classify_data(sys.argv[1], 'preprocessed_train.txt')
#	classify_data(sys.argv[2], 'preprocessed_test.txt')

#	with open("results.txt", "w") as output_file:
#		for k, v in sorted(vocab.items()):
#			output_file.write(k + " " + str(v).strip("[]") + "\n")


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: " + sys.argv[0] + " <training file> <test file>"
		exit()
	main()
