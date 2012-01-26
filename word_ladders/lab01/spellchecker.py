#
# Torbert, 11 August 2011
#
# First week example Python program... spell checker
#
#   Input: dictionary of six-letter words and a string entered by the user
# Process: determine if the user's string is a word in the dictionary
#  Output: indicate YES or NO, and if YES then also indicate which SLOT
#
wlist=open('words.txt','r').read().split()
ustr=raw_input('String: ')
#
flag=False
k=0
while k<len(wlist):
	#
	if wlist[k]==ustr:
		flag=True
		break
	#
	k+=1
#
if flag:
	print 'Yes, %s is a word.  In fact, it\'s in slot %d.'%(ustr,k)
else:
	print 'No,',ustr,'is not a word.'
#
# end of file
#
