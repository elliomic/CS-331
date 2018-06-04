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


def preprocess(infile, outfile):
	feature_table = dict()
	classlabel = []

	num_lines = file_len(infile)
	with open(infile, "r") as input_file:
		current_line = 0
		for line in input_file:
			line = line.split()
			classlabel.append(line[-1])
			sentiment = line[-1] == "1"

			for word in line[:-1]:
				word = word.lower().translate(None, string.punctuation+string.digits)
				if word == "":
					continue

				try:
					feature_table[word][current_line] = 1
				except:
					feature_table[word] = [0 for i in xrange(num_lines)]
					feature_table[word][current_line] = 1

			current_line += 1

	current_file = open(outfile, 'w')
	pp = pprint.PrettyPrinter(indent = 4, stream = current_file)
	pp.pprint(feature_table)

	return feature_table, classlabel


def classify(training_set, classlabel, test_set, testlabel):
	vocab = dict()
	res_label = []
	total_pos, total_neg = (0.0, 0.0)
	for key in training_set:
		pos, neg = (0, 0)
		for i in xrange(0, len(classlabel)):
			if training_set[key][i] == 1:
				sentiment = classlabel[i] == '1'
				if sentiment:
					pos += 1
					total_pos += 1
				else:
					neg += 1
					total_neg += 1
		vocab[key] = (pos, neg)
	total_prob = total_pos/(total_pos+total_neg)
	
	for i in xrange(0, len(testlabel)):
		pos_prob = total_prob
		neg_prob = 1 - total_prob
		for key in test_set:
			pos_sum = 0.0
			neg_sum = 0.0
			if(test_set[key][i] == 1):
				try:
					pos_sum += vocab[key][0]
					neg_sum += vocab[key][1]

					pos_prob *= pos_sum/(pos_sum + neg_sum) 
					neg_prob *= neg_sum/(pos_sum + neg_sum)
				except:
					pass

		if(pos_prob > neg_prob):
			res_label.append('1')
		else:
			res_label.append('0')

	count = 0
	for i in range(0, len(res_label)):
		if(res_label[i] == testlabel[i]):
			count += 1
		
	return str(count) + " correct out of " + str(len(res_label)) + "\t\t" + str(round(count*100.0/len(res_label), 1)) + "% correct"


def main(): 
	training_set, training_classifications = preprocess(sys.argv[1], 'preprocessed_train.txt')
	test_set, test_classifications = preprocess(sys.argv[2], 'preprocessed_test.txt')
	training_result = sys.argv[1] + ":\t" + classify(training_set, training_classifications, training_set, training_classifications)
	test_result = sys.argv[2] + ":\t\t" + classify(training_set, training_classifications, test_set, test_classifications)

	print training_result
	print test_result

	with open("results.txt", 'w') as result_file:
		result_file.write(training_result + '\n')
		result_file.write(test_result + '\n')


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: " + sys.argv[0] + " <training file> <test file>"
		exit()
	main()
