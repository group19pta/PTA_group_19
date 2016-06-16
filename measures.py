#!/usr/bin/env python3

from collections import Counter
from nltk.metrics import ConfusionMatrix
import os
import nltk


print("\nPrecision, recall, fscore for entity or non-entity\n")
tokens1 = []
tokens2 = []


#HIER MOET HET PATH NAAR ONS PROGRAMMA KOMEN
path1 = '/home/zoo/Documents/PTA/training2'
directories = []
for i in os.listdir(path1):
    file = "/" + i 
    directories.append(file)
for i in directories:
    for directory in os.listdir(path1 + i):
        if directory[0] =='d':
          with open(path1 + i + "/" + directory + '/en.tok.off.pos.ent', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    words = line.split()
                    if len(words)<6:
                        tokens1.append("NON_ENTITY")
                    else:
                        tokens1.append("ENTITY")

#DIT IS DE GOLD STANDARD
path2 = '/home/zoo/Documents/PTA/training'
directories = []
for i in os.listdir(path2):
    file = "/" + i
    directories.append(file)
for i in directories:
    for directory in os.listdir(path2 + i):
        if directory[0] =='d':
            with open(path2 + i + "/" + directory + '/en.tok.off.pos.ent', 'r') as file:      
                lines = file.readlines()
                for line in lines:
                    words = line.split()
                    if len(words)<6:
                        tokens2.append("NON_ENTITY")
                    else:
                        tokens2.append("ENTITY")

print(len(tokens1))
print(len(tokens2))
ref  = tokens1
tagged = tokens2
cm = ConfusionMatrix(ref, tagged)

labels = set('NON_ENTITY ENTITY'.split())

true_positives = Counter()
false_negatives = Counter()
false_positives = Counter()

for i in labels:
    for j in labels:
        if i == j:
            true_positives[i] += cm[i,j]
        else:
            false_negatives[i] += cm[i,j]
            false_positives[j] += cm[i,j]

print("TP:", sum(true_positives.values()), true_positives)
print("FN:", sum(false_negatives.values()), false_negatives)
print("FP:", sum(false_positives.values()), false_positives)
print() 

for i in sorted(labels):
    if true_positives[i] == 0:
        fscore = 0
    else:
        precision = true_positives[i] / float(true_positives[i]+false_positives[i])
        recall = true_positives[i] / float(true_positives[i]+false_negatives[i])
        fscore = 2 * (precision * recall) / float(precision + recall)

    print("\n", i,"\nPrecision", precision, "\nRecall", recall, "\nFscore", fscore)


print("\nPrecision, recall, fscore for specific entities\n")
tokens1 = []
tokens2 = []


#HIER MOET HET PATH NAAR ONS PROGRAMMA KOMEN
path1 = '/home/zoo/Documents/PTA/training2'
directories = []
for i in os.listdir(path1):
    file = "/" + i
    directories.append(file)
for i in directories:
    for directory in os.listdir(path1 + i):
          if directory[0] =='d':
            with open(path1 + i + "/" + directory + '/en.tok.off.pos.ent', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    words = line.split()
                    if len(words)<6:
                        tokens1.append("NON_ENTITY")
                    else:
                        tokens1.append(words[5])


#DIT IS DE GOLD STANDARD
path2 = '/home/zoo/Documents/PTA/training'
directories = []
for i in os.listdir(path2):
    file = "/" + i
    directories.append(file)
for i in directories:
    for directory in os.listdir(path2 + i):
        if directory[0] =='d':
            with open(path2 + i + "/" + directory + '/en.tok.off.pos.ent', 'r') as file:        
                lines = file.readlines()
                for line in lines:
                    words = line.split()
                    if len(words)<6:
                        tokens2.append("NON_ENTITY")
                    else:
                        tokens2.append(words[5])
               
ref  = tokens1
tagged = tokens2
cm = ConfusionMatrix(ref, tagged)


labels = set('NON_ENTITY ANI CIT COU ENT NAT ORG PER SPO'.split())

true_positives = Counter()
false_negatives = Counter()
false_positives = Counter()

for i in labels:
    for j in labels:
        if i == j:
            true_positives[i] += cm[i,j]
        else:
            false_negatives[i] += cm[i,j]
            false_positives[j] += cm[i,j]

print("TP:", sum(true_positives.values()), true_positives)
print("FN:", sum(false_negatives.values()), false_negatives)
print("FP:", sum(false_positives.values()), false_positives)
print() 

for i in sorted(labels):
    if true_positives[i] == 0:
        fscore = 0
    else:
        precision = true_positives[i] / float(true_positives[i]+false_positives[i])
        recall = true_positives[i] / float(true_positives[i]+false_negatives[i])
        fscore = 2 * (precision * recall) / float(precision + recall)

    print("\n", i,"\nPrecision", precision, "\nRecall", recall, "\nFscore", fscore)


print("\nConfusion matrix")
print(cm)

