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
posList=['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNP','PDT','POS','PRP','PRP','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB']
token_tweet_list = []
polarity_list = []
token_tweet_test_list = []
polarity_test_list = []

#Global Variables for extra features
num_all_caps = []
num_all_pun = []
num_all_lastpun = []
num_all_neg = []
num_all_hashtag = []
num_all_lastemo = []
num_all_posemo = []
num_all_negemo = []
num_all_rep = []
num_all_scoregr0 = []
num_all_scoresum = []
num_all_maxscore = []
num_all_lastnzscore = []
num_all_firstnzscore = []
posvaL = []

tmpL = fp.readlines()
tpolL = fp2.readlines()

for i in range(len(tmpL)):
	if len(tmpL[i].strip('\n')) > 0:
		token_tweet_list.append(tmpL[i].strip('\n'))
		polarity_list.append(tpolL[i].strip('\n'))

#Extra Features
def extra_features(tweet_list,posFile):
	print "Entered the extra_features function"
	len_list = len(tweet_list)
#elongated words: the number of words with one character repeated more than 2 times, e.g. 'soooo';
	global num_all_rep
	num_all_rep = [0 for i in range(len_list)]
	pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
	tweetcount=0
	for tweet in tweet_list:
		for match in re.finditer(pattern, tweet):
			num_all_rep[tweetcount]+=1
		tweetcount+=1

#presence/absence of positive and negative emoticons at any position in the tweet; 
	global num_all_posemo
	num_all_posemo = [0 for i in range(len_list)]
	global num_all_negemo
	num_all_negemo = [0 for i in range(len_list)]
	tweetcount=0
	for tweet in tweet_list:
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
	global num_all_lastemo
	num_all_lastemo = [0 for i in range(len_list)]
	tweetcount=0
	for tweet in tweet_list:
		tokens = tweet.split(' ')
		last_token = tokens[len(tokens)-1]
		if(last_token == 'epositive'):
			num_all_lastemo[tweetcount] = 1
		elif(last_token == 'enegative'):
			num_all_lastemo[tweetcount] = -1

#hashtags: the number of hashtags;
	global num_all_hashtag
	num_all_hashtag = [0 for i in range(len_list)]
	tweetcount=0
	for tweet in tweet_list:
		tokens = tweet.split(' ')
		for token in tokens:
			if(re.search('^#.*',token)):
				num_all_hashtag[tweetcount]+=1
		tweetcount+=1

#negation: the number of negated contexts
	global num_all_neg
	num_all_neg = [0 for i in range(len_list)]
	tweetcount=0
	for tweet in tweet_list:
		tokens = tweet.split(' ')
		for i in range(0,len(tokens)):
			if(tokens[i]=='not'):
				num_all_neg[tweetcount]+=1
				if(i < len(tokens)-1) and tokens[i+1].isalpha():
					tokens[i+1]+='_neg'
		tweetcount+=1

#POS: the number of occurrences for each part-of-speech tag;
	fpos=open('../preprocessor/'+posFile,"r")
	tmpPosL = fpos.readlines()
	global posvaL
	posvaL = [[0]*len(posList) for i in range(len_list)]
	tweetcount = 0
	for tweet in tmpPosL:
		tmp = tweet.strip('\n').split(' ')
		for val in tmp:
			if(len(val)):
				posvaL[tweetcount][posList.index(val.split("<:>")[1])] += 1
		tweetcount += 1
	fpos.close()

#- punctuation:
#the number of contiguous sequences of exclamation marks, question marks, and both exclamation and question marks;
	global num_all_pun
	num_all_pun = [0 for i in range(len_list)]
	tweetcount=0
	for tweet in tweet_list:
		for match in re.finditer('[?!]{2,}', tweet):
			num_all_pun[tweetcount]+=1
		tweetcount+=1
	#whether the last token contains exclamation or question mark;
	global num_all_lastpun
	num_all_lastpun = [0 for i in range(len_list)]
	tweetcount=0
	for tweet in tweet_list:
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
	global num_all_scoregr0
	num_all_scoregr0 = [0 for i in range(len_list)]
	tweetcount=0
	for tweet in tweet_list:
		tokens = tweet.split(' ')
		for token in tokens:
			if token in sentiments:
				if(sentiments[token]>0):
					num_all_scoregr0[tweetcount]+=1
		tweetcount+=1

#the sum of the scores for all tokens in the tweet;
	global num_all_scoresum
	num_all_scoresum = [0 for i in range(len_list)]
	tweetcount=0
	for tweet in tweet_list:
		tokens = tweet.split(' ')
		for token in tokens:
			if token in sentiments:
				num_all_scoresum[tweetcount]+=float(sentiments[token])
			if token.endswith("_neg") and token[0:-4] in sentiments:
				num_all_scoresum[tweetcount]-=float(sentiments[token[0:-4]])
		tweetcount+=1

#the maximal score;
	global num_all_maxscore
	num_all_maxscore = [-100000 for i in range(len_list)]
	tweetcount=0
	for tweet in tweet_list:
		tokens = tweet.split(' ')
		for token in tokens:
			if token in sentiments:
				if(num_all_maxscore[tweetcount]<sentiments[token]):
					num_all_maxscore[tweetcount]=float(sentiments[token])
		if(num_all_maxscore[tweetcount]==-100000):
			num_all_maxscore[tweetcount]=0
		tweetcount+=1

#the non-zero score of the last token in the tweet;
	global num_all_lastnzscore
	num_all_lastnzscore = [0 for i in range(len_list)]
	tweetcount=0
	for tweet in tweet_list:
		tokens = tweet.split(' ')
		for i in range(len(tokens)-1,-1,-1):
			if tokens[i] in sentiments:
				if(sentiments[tokens[i]]!=0):
					num_all_lastnzscore[tweetcount]=float(sentiments[tokens[i]])
					break
		tweetcount+=1

#the non-zero score of the first token in the tweet;
	global num_all_firstnzscore
	num_all_firstnzscore = [0 for i in range(len_list)]
	tweetcount=0
	for tweet in tweet_list:
		tokens = tweet.split(' ')
		for i in range(0,len(tokens)):
			if tokens[i] in sentiments:
				if(sentiments[tokens[i]]!=0):
					num_all_firstnzscore[tweetcount]=float(sentiments[tokens[i]])
					break
		tweetcount+=1
	   
#Caps Feature
	global num_all_caps
	num_all_caps = [0 for i in range(len_list)]
	tweetcount = 0
	for tweet in tweet_list:
		tokenlist_tweet = tweet.split(' ')
		for token in tokenlist_tweet:
			if token.isalpha() and token.isupper():
				num_all_caps[tweetcount] += 1
		tweetcount +=1


#Compute the Extra Features:
extra_features(token_tweet_list,"TrainWithPos")

#Build the Unigram Dictionary of Words
tweetcount = 0
for tweet in token_tweet_list:
	tokenlist_tweet = tweet.split(' ')
	for token in tokenlist_tweet:
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

print len(num_all_caps)

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
			indx_L.append(indx+1)
	dict = {}
	for indx in indx_L:
		if indx in dict:
			dict[indx] += 1
		else:
			dict[indx] = 1
	T = sorted(dict.items(), key=lambda s: s[0])
	for val in T:
		trstr += " "+str(val[0])+":"+str(val[1])
	#If the tweet is not empty, Add the list of extra Features
	cur_indx = len_dict + 1
	if len(trstr) > 0:
		if num_all_caps[tweetcount]:	#Add Caps Feature
			trstr += " "+str(cur_indx)+":"+str(num_all_caps[tweetcount])
		cur_indx += 1
		if num_all_pun[tweetcount]:	#Num of contiguous Exclamations
			trstr += " "+str(cur_indx)+":"+str(num_all_pun[tweetcount])
		cur_indx += 1
		if num_all_lastpun[tweetcount]:	#Whether Last token contains Punctuation
			trstr += " "+str(cur_indx)+":"+str(num_all_lastpun[tweetcount])
		cur_indx += 1
		if num_all_neg[tweetcount]:	#Number of Negated Contexts
			trstr += " "+str(cur_indx)+":"+str(num_all_neg[tweetcount])
		cur_indx += 1
		if num_all_hashtag[tweetcount]:	#Number of Hashtags
			trstr += " "+str(cur_indx)+":"+str(num_all_hashtag[tweetcount])
		cur_indx += 1
		if num_all_lastemo[tweetcount]:	#If last token is an emoticon
			trstr += " "+str(cur_indx)+":"+str(num_all_lastemo[tweetcount])
		cur_indx += 1
		if num_all_posemo[tweetcount]:	#Num of +ve emoticon
			trstr += " "+str(cur_indx)+":"+str(num_all_posemo[tweetcount])
		cur_indx += 1
		if num_all_negemo[tweetcount]:	#Num of -ve emoticon
			trstr += " "+str(cur_indx)+":"+str(num_all_negemo[tweetcount])
		cur_indx += 1
		if num_all_rep[tweetcount]:	#Num of elongated words
			trstr += " "+str(cur_indx)+":"+str(num_all_rep[tweetcount])
		cur_indx += 1
		#Sentiment Lexicons Start here:
		if num_all_scoregr0[tweetcount]:	#Num of lexicons with score > 0
			trstr += " "+str(cur_indx)+":"+str(num_all_scoregr0[tweetcount])
		cur_indx += 1
		if num_all_scoresum[tweetcount]:	#Sum of scores of all lexicons
			trstr += " "+str(cur_indx)+":"+str(num_all_scoresum[tweetcount])
		cur_indx += 1
		if num_all_maxscore[tweetcount]:	#Max of scores of all lexicons
			trstr += " "+str(cur_indx)+":"+str(num_all_maxscore[tweetcount])
		cur_indx += 1
		if num_all_lastnzscore[tweetcount]:	#non-zero score of last token
			trstr += " "+str(cur_indx)+":"+str(num_all_lastnzscore[tweetcount])
		cur_indx += 1
		if num_all_firstnzscore[tweetcount]:	#non-zero score of first token
			trstr += " "+str(cur_indx)+":"+str(num_all_firstnzscore[tweetcount])
		cur_indx += 1
		#Add the Count of Pos here
		for poscnt in posvaL[tweetcount]:
			if poscnt:
				trstr += " "+str(cur_indx)+":"+str(poscnt)
			cur_indx += 1
		trf.write(trstr+"\n")
	tweetcount += 1

tmpL = fpt.readlines()
tpolL = fpt2.readlines()

for i in range(len(tmpL)):
	if len(tmpL[i].strip('\n')) > 0:
		token_tweet_test_list.append(tmpL[i].strip('\n'))
		polarity_test_list.append(tpolL[i].strip('\n'))

extra_features(token_tweet_test_list,"Test1000WithPos")
expected_class = []

tweetcount = 0
for tweet in token_tweet_test_list:
	tokenlist_tweet = tweet.split(' ')
	tsstr = ""
	indx_L = []
	if polarity_test_list[tweetcount] == 'positive':
		tsstr += str(1)
	elif polarity_test_list[tweetcount] == 'negative':
		tsstr += str(2)
	else:
		tsstr += str(0)

	for token in tokenlist_tweet:
		token = token.lower()
		if token in dict_final_tokens:
			indx = dict_final_tokens.index(token)
			indx_L.append(indx+1)
	dict = {}
	for indx in indx_L:
		if indx in dict:
			dict[indx] += 1
		else:
			dict[indx] = 1
	T = sorted(dict.items(), key=lambda s: s[0])
	for val in T:
		tsstr += " "+str(val[0])+":"+str(val[1])
	#If the tweet is not empty, Add the list of extra Features
	cur_indx = len_dict + 1
	if len(tsstr) > 0:
		if num_all_caps[tweetcount]:	#Add Caps Feature
			tsstr += " "+str(cur_indx)+":"+str(num_all_caps[tweetcount])
		cur_indx += 1
		if num_all_pun[tweetcount]:	#Num of contiguous Exclamations
			tsstr += " "+str(cur_indx)+":"+str(num_all_pun[tweetcount])
		cur_indx += 1
		if num_all_lastpun[tweetcount]:	#Whether Last token contains Punctuation
			tsstr += " "+str(cur_indx)+":"+str(num_all_lastpun[tweetcount])
		cur_indx += 1
		if num_all_neg[tweetcount]:	#Number of Negated Contexts
			tsstr += " "+str(cur_indx)+":"+str(num_all_neg[tweetcount])
		cur_indx += 1
		if num_all_hashtag[tweetcount]:	#Number of Hashtags
			tsstr += " "+str(cur_indx)+":"+str(num_all_hashtag[tweetcount])
		cur_indx += 1
		if num_all_lastemo[tweetcount]:	#If last token is an emoticon
			tsstr += " "+str(cur_indx)+":"+str(num_all_lastemo[tweetcount])
		cur_indx += 1
		if num_all_posemo[tweetcount]:	#Num of +ve emoticon
			tsstr += " "+str(cur_indx)+":"+str(num_all_posemo[tweetcount])
		cur_indx += 1
		if num_all_negemo[tweetcount]:	#Num of -ve emoticon
			tsstr += " "+str(cur_indx)+":"+str(num_all_negemo[tweetcount])
		cur_indx += 1
		if num_all_rep[tweetcount]:	#Num of elongated words
			tsstr += " "+str(cur_indx)+":"+str(num_all_rep[tweetcount])
		cur_indx += 1
		#Sentiment Lexicons Start here:
		if num_all_scoregr0[tweetcount]:	#Num of lexicons with score > 0
			tsstr += " "+str(cur_indx)+":"+str(num_all_scoregr0[tweetcount])
		cur_indx += 1
		if num_all_scoresum[tweetcount]:	#Sum of scores of all lexicons
			tsstr += " "+str(cur_indx)+":"+str(num_all_scoresum[tweetcount])
		cur_indx += 1
		if num_all_maxscore[tweetcount]:	#Max of scores of all lexicons
			tsstr += " "+str(cur_indx)+":"+str(num_all_maxscore[tweetcount])
		cur_indx += 1
		if num_all_lastnzscore[tweetcount]:	#non-zero score of last token
			tsstr += " "+str(cur_indx)+":"+str(num_all_lastnzscore[tweetcount])
		cur_indx += 1
		if num_all_firstnzscore[tweetcount]:	#non-zero score of first token
			tsstr += " "+str(cur_indx)+":"+str(num_all_firstnzscore[tweetcount])
		cur_indx += 1
		#Add the Count of Pos here
		for poscnt in posvaL[tweetcount]:
			if poscnt:
				tsstr += " "+str(cur_indx)+":"+str(poscnt)
			cur_indx += 1
		tsf.write(tsstr+"\n")
		expected_class.append(tsstr[0])
	tweetcount += 1

fp.close()
fp2.close()
fpt.close()
fpt2.close()
trf.close()
tsf.close()
