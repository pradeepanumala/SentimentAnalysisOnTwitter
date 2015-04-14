from nltk import pos_tag, word_tokenize
posList=['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNP','PDT','POS','PRP','PRP'
         ,'RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB']
inFile=open("testTweets.txt",'r')
## Assuming the input file is in the same directory of the script
outFile = open("TweetsWithPos.txt","w+")
## output file is created in the same directory
tweets = inFile.readlines()
for tweet in tweets:
    tweetWithPosList = pos_tag(word_tokenize(tweet))
    for tweetList in tweetWithPosList:
        if tweetList[1] in posList:
            outFile.write(tweetList[0] +":" +tweetList[1]+" ")
    outFile.write("\n")

inFile.close()
outFile.close()
            
##testTweets.txt -- inFile
##Hello my name is Derek. I live in Salt Lake city.
##Hi all. How are you ?
##It's raining cats and dogs here in hyderabad.
##
##TweetsWithPos.txt -- outFile
##Hello:NNP name:NN is:VBZ Derek:NNP I:PRP live:VBP in:IN Salt:NNP Lake:NNP city:NN 
##Hi:NNP all:DT How:WRB are:VBP you:PRP 
##It:PRP 's:VBZ raining:VBG cats:NNS and:CC dogs:NNS here:RB in:IN hyderabad:JJ 
##

##	1.	CC	Coordinating conjunction
##	2.	CD	Cardinal number
##	3.	DT	Determiner
##	4.	EX	Existential there
##	5.	FW	Foreign word
##	6.	IN	Preposition or subordinating conjunction
##	7.	JJ	Adjective
##	8.	JJR	Adjective, comparative
##	9.	JJS	Adjective, superlative
##	10.	LS	List item marker
##	11.	MD	Modal
##	12.	NN	Noun, singular or mass
##	13.	NNS	Noun, plural
##	14.	NNP	Proper noun, singular
##	15.	NNPS	Proper noun, plural
##	16.	PDT	Predeterminer
##	17.	POS	Possessive ending
##	18.	PRP	Personal pronoun
##	19.	PRP$	Possessive pronoun
##	20.	RB	Adverb
##	21.	RBR	Adverb, comparative
##	22.	RBS	Adverb, superlative
##	23.	RP	Particle
##	24.	SYM	Symbol
##	25.	TO	to
##	26.	UH	Interjection
##	27.	VB	Verb, base form
##	28.	VBD	Verb, past tense
##	29.	VBG	Verb, gerund or present participle
##	30.	VBN	Verb, past participle
##	31.	VBP	Verb, non-3rd person singular present
##	32.	VBZ	Verb, 3rd person singular present
##	33.	WDT	Wh-determiner
##	34.	WP	Wh-pronoun
##	35.	WP$	Possessive wh-pronoun
##	36.	WRB	Wh-adverb
