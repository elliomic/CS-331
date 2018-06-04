#!/usr/bin/python
"""
CS 331 Assignment #3: Sentiment Analysis
Anish Asrani, Michael Elliott
"""
import sys, string
#import pandas as pd
import itertools as it

def file_len(fname):
    with open(fname, "r") as f:
		return sum(1 for line in f)

def classify_data(infile, outfile):
	vocab = dict()
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

	matrix = zip(*[value if isinstance(value, list) else it.repeat(value) for key, value in vocab.items()])
	with open(outfile, "w") as output_file:
		output_file.write(''.join(['{:5}'.format(key) for key in vocab.keys()]))
		for row in matrix:
			output_file.write(''.join(['{:5}'.format(str(item)) for item in row]))
#	df = pd.DataFrame(vocab)
#	df['classlabel'] = classlabel
#	pd.set_option('display.max_rows', None)
#	df.to_csv(outfile, sep='\t', encoding='utf-8')

def main(): 
	classify_data(sys.argv[1], 'preprocessed_train.txt')
	classify_data(sys.argv[2], 'preprocessed_test.txt')

#	with open("results.txt", "w") as output_file:
#		for k, v in sorted(vocab.items()):
#			output_file.write(k + " " + str(v).strip("[]") + "\n")


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: " + sys.argv[0] + " <training file> <test file>"
		exit()
	main()
