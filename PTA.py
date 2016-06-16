#!/usr/bin/env python3

import os
import nltk
from nltk.tag.stanford import StanfordNERTagger
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import wikipedia
from nltk.wsd import lesk

def stanford_tagger(path, newpath):
	directories = []
	st = StanfordNERTagger('stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz','stanford-ner-2014-06-16/stanford-ner-3.4.jar')
	for i in os.listdir(path):
		file = "/" + i
		directories.append(file)

	wordlist = []
	for i in directories:
		for directory in os.listdir(path + i):
			if directory[0] =='d':
				with open(path + i + "/" + directory + '/en.tok.off.pos', 'r') as file:
					lines = file.readlines()
					for line in lines:
						words = line.split()
						if len(words) >= 5:
							wordlist.append(words[3])

	nieuw = ''
	tags = st.tag(wordlist)
	t = 0
	for i in directories:
		for directory in os.listdir(path + i):
			if directory[0] =='d':
				with open(path + i + "/" + directory + '/en.tok.off.pos', 'r') as file:
					nieuw = ''
					lines = file.readlines()
					for line in lines:
						words = line.split()
						if len(words) >= 5:
							tag = tags[t][1]
							if tag == 'PERSON':
								words.append('PER')

							elif tag == 'ORGANIZATION':
								words.append('ORG')

							elif tag == 'LOCATION':
								words.append('LOC')

							line = ' '.join(words)
							nieuw = nieuw + line + '\n'
							t = t + 1

					with open(newpath + i + "/"+ directory + '/en.tok.off.pos.ent', 'w') as newfile:
						newfile.write(nieuw)

def wordnet_tagger(path):
	directories = []

	for i in os.listdir(path):
		file = "/" + i
		directories.append(file)

	animal = wn.synset('animal.n.01')
	sport = wn.synset('sport.n.01')
	country = wn.synset('country.n.02')
	city = wn.synset('city.n.01')

	for i in directories:
		for directory in os.listdir(path + i):
			if directory[0] =='d':
				with open(path + i + "/" + directory + '/en.tok.off.pos.ent', 'r') as file:
					nieuw = ''
					lines = file.readlines()
					for line in lines:
						words = line.split()
						if words[4][0] == 'N':
							if len(words) == 5:
								synsets = wn.synsets(words[3])
								if len(synsets) >=1:
									synset = synsets[0].lowest_common_hypernyms(animal)
									synset2 = synsets[0].lowest_common_hypernyms(sport)
									if len(synset) >=1:
										synset = synset[0].name()
										if synset[0] == 'a':
											words.append('ANI')

										synset2 = synset2[0].name()
										if synset2[0] == 's':
											words.append('SPO')

						if len(words) >=6:
							if words[5][0] == 'L':
								synsets = wn.synsets(words[3])
								if len(synsets) >=1:
									synset = synsets[0].lowest_common_hypernyms(country)
									synset2 = synsets[0].lowest_common_hypernyms(city)
									if len(synset) >=1:
										synset = synset[0].name()
										if synset[0] == 'c':
											words[5] = ('COU')

										synset2 = synset2[0].name()
										if synset2[0] == 'c':
											words[5] = ('CIT')

								if words[5][0] == 'L':
									words[5] = 'NAT'

						line = ' '.join(words)
						nieuw = nieuw + line + "\n"
					with open(path + i + "/"+ directory + '/en.tok.off.pos.ent', 'w') as newfile:
						newfile.write(nieuw)

def wiki_linking(path):
	directories = []
					
	for i in os.listdir(path):
		file = "/" + i
		directories.append(file)

	for i in directories:
		for directory in os.listdir(path + i):
			if directory[0] =='d':
				with open(path + i + "/" + directory + '/en.tok.off.pos.ent', 'r') as file:
					lines = file.readlines()
					nieuw = ''
					nextlink = ''
					counter = 0
					counter2 = -2

					for line in lines:
						oldline = ''
						counter = counter + 1
						counter2 = counter2 + 1
						words = line.split()
						newline = line.split()
						if len(lines) <= counter:
							counter = 0

						if counter2 >=0:
							oldline = lines[counter2].split()

						if not nextlink == '':
							words.append(nextlink)
							line = ' '.join(words)

						nextline = lines[counter].split()
						nextlink = ''
						if len(newline) == 6 and len(nextline) == 6:
							if newline[5] == nextline[5]:
								title = newline[3] + ' ' + nextline[3]
								try:
									page = wikipedia.page(title=title, auto_suggest = True)
									link = page.url
									words.append(link)
									line = ' '.join(words)
									nextlink = link

								except wikipedia.exceptions.DisambiguationError as e:
									pass
								except wikipedia.exceptions.PageError:
									pass

						elif len(words) == 6:
							try:
								page = wikipedia.page(title=words[3], auto_suggest = True)
								link = page.url
								words.append(link)
								line = ' '.join(words)

							except wikipedia.exceptions.DisambiguationError as e:
								pass
							except wikipedia.exceptions.PageError:
								pass

						else:
							line = ' '.join(words)
						
						nieuw = nieuw + line.rstrip() + "\n"
					with open(path + i + "/"+ directory + '/en.tok.off.pos.ent', 'w') as newfile:
						newfile.write(nieuw)


def main():
	path = '/home/zoo/Documents/PTA/pta/training'
	newpath = '/home/zoo/Documents/PTA/pta/training2'
	stanford_tagger(path, newpath)
	wordnet_tagger(newpath)
	wiki_linking(newpath)


main()