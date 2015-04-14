import sys

f = open(sys.argv[1], "r")
n = 0
if int(sys.argv[2]) == 1:
	n = 2 #score for positive words
elif int(sys.argv[2]) == -1:
	n = -2 #score for negative words
else:
	print "Enter either 1 or -1"
	sys.exit(0)


for line in f:
	temp = line[:-1]
	print temp, n

f.close()
	
