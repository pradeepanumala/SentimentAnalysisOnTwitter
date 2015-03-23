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

unigram_matrix = [[0]*len(dict_final_tokens) for i in range(len_training)]

tweetcount = 0
for tweet in token_tweet_list:
	tokenlist_tweet = tweet.strip('\n').split(' ')
	for token in tokenlist_tweet:
		token = token.lower()
		if token in dict_final_tokens:
			indx = dict_final_tokens.index(token)
			unigram_matrix[tweetcount][indx] = 1
	tweetcount +=1

#print dict_final_tokens

#print "The final matrix is:\t", unigram_matrix
