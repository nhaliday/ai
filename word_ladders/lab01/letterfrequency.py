#
# Torbert, 11 August 2011
#
# First week example Python program... letter frequency
#
#   Input: dictionary of six-letter words
# Process: determine the frequency of each letter across the entire dictionary
#  Output: each letter A-Z and their total number of appearances in all words
#
from string import lowercase
#
wlist=open('words.txt','r').read().split()
#
freq={}                  # hash table
#
for w in wlist:          # loop over all words in word list
	#
	for ch in w:          # loop over all letters in each word
		#
		if ch not in freq: # have we already seen this letter ?
			freq[ch]  = 1
		else:
			freq[ch] += 1
		#
	#
#
for ch in lowercase:     # in Windows use lowercase[:26] instead
	print '%s %4d'%(ch,freq[ch])
#
# end of file
#
