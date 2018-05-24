#!/usr/bin/python
"""
CS 331 Assignment #3: Sentiment Analysis
Anish Asrani, Michael Elliott
"""
import sys, string


def vocabOrderBy(vocabEntry):
	key, (pos, neg) = vocabEntry
	return pos+neg


def main():
	vocab = dict()
	
	with open(sys.argv[1], "r") as input_file:
		for line in input_file:
			line = line.split()
			sentiment = line[-1] == "1"
			for word in line[:-1]:
				word = word.lower().translate(None, string.punctuation+string.digits)
				if word == "":
					continue

				if word not in vocab:
					vocab[word] = (0, 0)

				pos, neg = vocab[word]
				if sentiment:
					vocab[word] = (pos+1, neg)
				else:
					vocab[word] = (pos, neg+1)
				
	with open(sys.argv[2], "w") as output_file:
		for k, v in sorted(vocab.items(), reverse=True, key=vocabOrderBy):
			output_file.write(k + " " + str(v) + "\n")


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: " + sys.argv[0] + " <input file> <output file>"
		exit()
	main()
