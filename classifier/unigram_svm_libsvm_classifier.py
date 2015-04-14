#coding=utf-8
#!/bin/bash
#Classifier based on Unigrams for sentiment analysis in Twitter

import sys
import re

fp = open("../tokenizer/preprocessed_tokens_train",'r')
fp2 = open("../tokenizer/polarity_train",'r')
fpt = open("../tokenizer/test_1000",'r')
fpt2 = open("../tokenizer/polarity_1000",'r')

dict_final_tokens = []

num_class = 3
classlist = ['positive','negative','neutral']
confusion_mat = [[0]*num_class for i in range(num_class)]

token_tweet_list = []
polarity_list = []
token_tweet_test_list = []
polarity_test_list = []

tmpL = fp.readlines()
tpolL = fp2.readlines()

for i in range(len(tmpL)):
	if len(tmpL[i].strip('\n')) > 0:
		token_tweet_list.append(tmpL[i].strip('\n'))
		polarity_list.append(tpolL[i].strip('\n'))

len_training = len(token_tweet_list)

#Extra Features

#elongated words: the number of words with one character repeated more than 2 times, e.g. 'soooo';
num_all_rep = [0 for i in range(len_training)]
pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
tweetcount=0
for tweet in token_tweet_list:
	for match in re.finditer(pattern, tweet):
		num_all_rep[tweetcount]+=1
	tweetcount+=1

#presence/absence of positive and negative emoticons at any position in the tweet; 
num_all_posemo = [0 for i in range(len_training)]
num_all_negemo = [0 for i in range(len_training)]
tweetcount=0
for tweet in token_tweet_list:
	tokens=tweet.split(' ')
	for token in tokens:
		if(token=='epositive'):
			num_all_posemo[tweetcount]=1
			break
	for token in tokens:
		if(token=='enegative'):
			num_all_negemo[tweetcount]=1
			break
	tweetcount+=1

#whether the last token is a positive or negative emoticon;
num_all_lastemo = [0 for i in range(len_training)]
tweetcount=0
for tweet in token_tweet_list:
	tokens = tweet.split(' ')
	last_token = tokens[len(tokens)-1]
	if(last_token == 'epositive'):
		num_all_lastemo[tweetcount] = 1
	elif(last_token == 'enegative'):
		num_all_lastemo[tweetcount] = -1

#hashtags: the number of hashtags;
num_all_hashtag = [0 for i in range(len_training)]
tweetcount=0
for tweet in token_tweet_list:
	tokens = tweet.split(' ')
	for token in tokens:
		if(re.search('^#.*',token)):
			num_all_hashtag[tweetcount]+=1
	tweetcount+=1

#negation: the number of negated contexts
num_all_neg = [0 for i in range(len_training)]
tweetcount=0
for tweet in token_tweet_list:
	tokens = tweet.split(' ')
	for i in range(0,len(tokens)):
		if(tokens[i]=='not'):
			num_all_neg[tweetcount]+=1
			if(i < len(tokens)-1):
				tokens[i+1]+='_neg'
	tweetcount+=1

#POS: the number of occurrences for each part-of-speech tag;

#- punctuation:
#the number of contiguous sequences of exclamation marks, question marks, and both exclamation and question marks;
num_all_pun = [0 for i in range(len_training)]
tweetcount=0
for tweet in token_tweet_list:
	for match in re.finditer('[?!]{2,}', tweet):
		num_all_pun[tweetcount]+=1
	tweetcount+=1
#whether the last token contains exclamation or question mark;
num_all_lastpun = [0 for i in range(len_training)]
tweetcount=0
for tweet in token_tweet_list:
	tokens = tweet.split(' ')
	last_token = tokens[len(tokens)-1]
	if(re.search('[?!]{1,}', last_token)):
		num_all_lastpun[tweetcount]=1
	tweetcount+=1

#- sentiment lexicons
sentiments = {}
file = '../dictionaries/sentiment140_lexicon/unigrams-pmilexicon.txt'
f = open(file,'r')
for line in f:
	line = line.split('\t')
	if(len(line) > 1):
		sentiments[line[0]] = line[1]
# total count of tokens in the tweet with score greater than 0;
num_all_scoregr0 = [0 for i in range(len_training)]
tweetcount=0
for tweet in token_tweet_list:
	tokens = tweet.split(' ')
	for token in tokens:
		if token in sentiments:
			if(sentiments[token]>0):
				num_all_scoregr0[tweetcount]+=1
	tweetcount+=1

#the sum of the scores for all tokens in the tweet;
num_all_scoresum = [0 for i in range(len_training)]
tweetcount=0
for tweet in token_tweet_list:
	tokens = tweet.split(' ')
	for token in tokens:
		if token in sentiments:
			num_all_scoresum[tweetcount]+=sentiments[token]
	tweetcount+=1

#the maximal score;
num_all_maxscore = [-100000 for i in range(len_training)]
tweetcount=0
for tweet in token_tweet_list:
	tokens = tweet.split(' ')
	for token in tokens:
		if token in sentiments:
			if(num_all_maxscore[tweetcount]<sentiments[token]):
				num_all_maxscore[tweetcount]=sentiments[token]
	if(num_all_maxscore[tweetcount]==-100000):
		num_all_maxscore[tweetcount]=0
	tweetcount+=1

#the non-zero score of the last token in the tweet;
num_all_lastnzscore = [0 for i in range(len_training)]
tweetcount=0
for tweet in token_tweet_list:
	tokens = tweet.split(' ')
	for i in range(len(tokens)-1,-1,-1):
		if tokens[i] in sentiments:
			if(sentiments[tokens[i]]!=0):
				num_all_lastnzscore[tweetcount]=sentiments[tokens[i]]
				break
	tweetcount+=1

#the non-zero score of the first token in the tweet;
num_all_firstnzscore = [0 for i in range(len_training)]
tweetcount=0
for tweet in token_tweet_list:
	tokens = tweet.split(' ')
	for i in range(0,len(tokens)):
		if tokens[i] in sentiments:
			if(sentiments[tokens[i]]!=0):
				num_all_firstnzscore[tweetcount]=sentiments[tokens[i]]
				break
	tweetcount+=1
	   
#Caps Feature
num_all_caps = [0 for i in range(len_training)]

tweetcount = 0
for tweet in token_tweet_list:
	tokenlist_tweet = tweet.split(' ')
	for token in tokenlist_tweet:
		if token.isalpha() and token.isupper():
			num_all_caps[tweetcount] += 1
		token = token.lower()
		if token.isalpha() and token not in dict_final_tokens:
			dict_final_tokens.append(token)
	tweetcount +=1

len_dict = len(dict_final_tokens)
print len_dict

dict_final_tokens.sort()

trf = open("training",'w+')
tsf = open("testing",'w+')

tweetcount = 0
#Positive:2934
#Neg:1120
#Neu:3821


for tweet in token_tweet_list:
	tokenlist_tweet = tweet.split(' ')
	trstr = ""
	indx_L = []
	if polarity_list[tweetcount] == 'positive':
		trstr += str(1)
	elif polarity_list[tweetcount] == 'negative':
		trstr += str(2)
	else:
		trstr += str(0)

	for token in tokenlist_tweet:
		token = token.lower()
		if token in dict_final_tokens:
			indx = dict_final_tokens.index(token)
			#if indx not in indx_L:
			indx_L.append(indx+1)
	dict = {}
	for indx in indx_L:
		if indx in dict:
			dict[indx] += 1
		else:
			dict[indx] = 1
	#indx_L.sort()
	T = sorted(dict.items(), key=lambda s: s[0])
	#for indx in indx_L:
	for val in T:
		trstr += " "+str(val[0])+":"+str(val[1])
	if len(trstr) > 1:	
		trstr += " "+str(len_dict+1)+":"+str(num_all_caps[tweetcount])
		trf.write(trstr+"\n")
	tweetcount += 1

tmpL = fpt.readlines()
tpolL = fpt2.readlines()

for i in range(len(tmpL)):
	if len(tmpL[i].strip('\n')) > 0:
		token_tweet_test_list.append(tmpL[i].strip('\n'))
		polarity_test_list.append(tpolL[i].strip('\n'))

len_testing = len(token_tweet_test_list)
#Extra Features
num_all_caps = [0 for i in range(len_testing)]
expected_class = []

tweetcount = 0
for tweet in token_tweet_test_list:
	tokenlist_tweet = tweet.split(' ')
	tsstr = ""
	indx_L = []
	if polarity_list[tweetcount] == 'positive':
		tsstr += str(1)
	elif polarity_list[tweetcount] == 'negative':
		tsstr += str(2)
	else:
		tsstr += str(0)

	for token in tokenlist_tweet:
		if token.isalpha() and token.isupper():
			num_all_caps[tweetcount] += 1
		token = token.lower()
		if token in dict_final_tokens:
			indx = dict_final_tokens.index(token)
			#if indx not in indx_L:
			indx_L.append(indx+1)
	dict = {}
	for indx in indx_L:
#		if dict_final_tokens[indx-1] in positive_words:
#			wt = 3
#		elif dict_final_tokens[indx-1] in negative_words:
#			wt = -3
#		elif dict_final_tokens[indx-1] == 'epositive':
#			wt = 5
#		elif dict_final_tokens[indx-1] == 'enegative':
#			wt = -5
#		else:
#			wt = 1
		if indx in dict:
			dict[indx] += 1
		else:
			dict[indx] = 1
	#indx_L.sort()
	T = sorted(dict.items(), key=lambda s: s[0])
	#for indx in indx_L:
	for val in T:
		tsstr += " "+str(val[0])+":"+str(val[1])
	if len(tsstr) > 1:
		tsstr += " "+str(len_dict+1)+":"+str(num_all_caps[tweetcount])	
		tsf.write(tsstr+"\n")
		expected_class.append(tsstr[0])
	tweetcount += 1

fp.close()
fp2.close()
fpt.close()
fpt2.close()
trf.close()
tsf.close()
