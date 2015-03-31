import os

datasetPath = "../dataset/"
f = open(datasetPath+'final_train.tsv', 'r')

messages = []
polarity = []
for line in f:
	tweet = line[:-1].split('\t')
	if(len(tweet) == 4):
		messages.append(tweet[3])
		polarity.append(tweet[2])
	elif(len(tweet) > 4):
		print "tab in tweet message"
		print tweet
		tme = ""
		for i in range(3,len(tweet)):
			tem += tweet[i]
		messages.append(tem)
		polarity.append(tweet[2])
	else:
		print "no. of tabs less than 4"
		print tweet

# for i in range(0,len(messages)):
# 	print messages[i] + " : " + polarity[i]
# 	print
f.close()

fname = './tweet-messages'
if(os.path.isfile(fname)):
	os.remove(fname)
f=open(fname, 'a')
for i in messages:
	if(i == 'Not Available'):
		continue
	f.write(i+'\n')
f.close()

fname = './polarity'
if(os.path.isfile(fname)):
	os.remove(fname)
f=open(fname, 'a')
for i in range(0,len(polarity)):
	if(messages[i] == 'Not Available'):
		continue
	f.write(polarity[i]+'\n')
f.close()
