#!/bin/bash
#Author : Shashank S
#Classifier based on Unigrams for sentiment analysis in Twitter

import sys

fp = open("tokens",'r')
fp2 = open("polarity",'r')
#fp2 = open("dict.txt",'w+')

stopwords = []

dict_map_key = []
dict_map_val = []
dict_final_tokens = []

token_tweet_list = fp.readlines()
polarity = fp2.readlines()
for i in range(0,len(polarity)):
	polarity[i]=polarity[i][:-1]
#print polarity

len_training = len(token_tweet_list)

ap = '\''

tokenlist_tweet = token_tweet_list[0].strip('\n').split(' ')

for tweet in token_tweet_list:
	tokenlist_tweet = tweet.strip('\n').split(' ')
	for token in tokenlist_tweet:
		token = token.lower()
		if token.isalpha() or ap in token:
			if not token in dict_final_tokens:
				dict_final_tokens.append(token)

dict_final_tokens.sort()

#unigram_matrix = [[0]*len(dict_final_tokens) for i in range(len_training)]

from sklearn.linear_model import SGDClassifier
clf = SGDClassifier()
tweetcount = 0
for tweet in token_tweet_list:
	print tweetcount
	unigram_matrix = [0]*len(dict_final_tokens)
	tokenlist_tweet = tweet.strip('\n').split(' ')
	for token in tokenlist_tweet:
		token = token.lower()
		if token in dict_final_tokens:
			indx = dict_final_tokens.index(token)
			unigram_matrix[indx] = 1
			clf.partial_fit([unigram_matrix],[polarity[tweetcount]], classes=['positive','negative','neutral'])
	tweetcount +=1

#print dict_final_tokens

#print "The final matrix is:\t", unigram_matrix

#from sklearn import svm
#clf = svm.LinearSVC()
#clf.fit(unigram_matrix,polarity)
#while(1):
#	print "Enter input : "
#	tweet=raw_input()
#	tweet = tweet.split(' ')
#	pred_matrix = [0]*len(dict_final_tokens)
#	for token in tweet:
#		token=token.lower()
#		if token in dict_final_tokens:
#			indx = dict_final_tokens.index(token)
#                        pred_matrix[indx] = 1
#	print clf.predict(pred_matrix)[0]

fname = './test_1000_polarity'
f = open(fname,'r')
test_polarity = f.readlines()
for i in range(0,len(test_polarity)):
	test_polarity[i] = test_polarity[i][:-1]
f.close()
fname = './test_1000_tokens'
f = open(fname,'r')
tweetcount=0
correct=wrong=0
for tweet in f:
	tweet=tweet[:-1]
        tweet = tweet.split(' ')
        pred_matrix = [0]*len(dict_final_tokens)
        for token in tweet:
                token=token.lower()
                if token in dict_final_tokens:
                        indx = dict_final_tokens.index(token)
                        pred_matrix[indx] = 1
        if(clf.predict(pred_matrix)[0] == test_polarity[tweetcount]):
		correct+=1
	else:
		wrong+=1
	tweetcount+=1
f.close()
print correct, wrong
