#!/usr/bin/python
"""
CS 331 Assignment #3: Sentiment Analysis
Anish Asrani, Michael Elliott
"""
import sys, string, pprint, collections
import itertools as it

def file_len(fname):
    with open(fname, "r") as f:
		return sum(1 for line in f)

def classify_data(infile, outfile):
	vocab = dict()
	train = collections.defaultdict(list)
	classlabel = []
	res_label = []

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
		for i in range(0, len(classlabel)-1):
			if vocab[key][i] == 1: 
				if classlabel[i] == '1':
					pos_count += 1
				elif classlabel[i] == '0':
					neg_count += 1
		train[key].append((pos_count, neg_count))

	for i in range(0, len(classlabel)-1):
		pos_sum = 0.0
		neg_sum = 0.0
		for key in vocab:
			if(vocab[key][i] == 1):
				pos_sum += train[key][0][0]
				neg_sum += train[key][0][1]

		if(pos_sum/(pos_sum+neg_sum) > neg_sum/(pos_sum+neg_sum)):
			res_label.append('1')
		else:
			res_label.append('0')

	count = 0
	for i in range(0, len(res_label)-1):
		if(res_label[i] == classlabel[i]):
			count += 1
		
	print("correct == " + str(count) + " out of === " + str(len(res_label)-1))


def main(): 
	classify_data(sys.argv[1], 'preprocessed_train.txt')
	classify_data(sys.argv[2], 'preprocessed_test.txt')


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: " + sys.argv[0] + " <training file> <test file>"
		exit()
	main()
