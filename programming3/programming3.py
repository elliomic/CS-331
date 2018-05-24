#!/usr/bin/python
"""
CS 331 Assignment #3: Sentiment Analysis
Anish Asrani, Michael Elliott
"""
import sys, string
import pandas as pd

def file_len(fname):
    with open(fname, "r") as f:
		return sum(1 for line in f)


def main(): 
	vocab = dict()
	classlabel = []
	
	num_lines = file_len(sys.argv[1])
	with open(sys.argv[1], "r") as input_file:
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

	df = pd.DataFrame(vocab)
	df['classlabel'] = classlabel
	pd.set_option('display.max_rows', None)
	df.to_csv('values.csv', sep=',', encoding='utf-8')
	
	with open("results.txt", "w") as output_file:
		for k, v in sorted(vocab.items()):
			output_file.write(k + " " + str(v).strip("[]") + "\n")


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: " + sys.argv[0] + " <training file> <test file>"
		exit()
	main()
