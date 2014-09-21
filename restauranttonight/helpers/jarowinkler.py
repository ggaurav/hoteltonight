def winkler_l(s1,s2, matchLength=4):
	""" Number of the four first characters matching """
	minlen = min(len(s1),len(s1))
	for same in range(minlen+1):
		if (s1[:same] != s2[:same]):
			break
	same -= 1
	if (same > matchLength):
		same = matchLength
	return same	

def jarow_m(s1,s2):
	""" Number of matching characters """
	m = 0
	d = {}
	for s in s1:
		d[s] = True
	for s in s2:
		if d.has_key(s):
			m += 1
	return m
def jarow_t(s1,s2):
	"""Number of transpositions"""
	t= 0
	pos ={}
	counter = 0
	for s in s1:
		pos[s] = counter
		counter += 1
	counter = 0
	for s in s2:
		if pos.has_key(s):
			if pos[s] != counter:
				t += 1
		counter += 1
	return t 	
	

def crap(s1,s2):	
	"""  Returns a number between 1 and 0, where 1 is the most similar
	    example:
	    print getSimilarity("martha","marhta")
	"""
	m= jarow_m(s1,s2)
	t1 = jarow_t(s1,s2)
	t2 = jarow_t(s2,s1)
	t = float(t1)/(float(t2) + 0.000001)
	d = 0.1
	# this is the jaro-distance
	d_j = 1.0/3.0 * ((m/len(s1)) + (m/len(s2)) + ((m - t)/float(m)))
	# if the strings are prefixed similar, they are weighted more heavily
	l = winkler_l(s1,s2)
	#print l
	return d_j + (l * 0.1 * (1 - d_j))

	
def getCommonCharacters(s1, s2, dist):
	ret = []
	copy = s2
	i=0
	l2 = len(s2)
	for ch in s1:
		found = False
		j=max(0, i-dist)
		while (not found) and j < min(i+dist, l2) :
		#	print '%d - %d - %s - %s - %s' % (i, j, copy, copy[j], ch)
			if copy[j] == ch :
				found=True
				ret.append(ch)
				copy=copy[:j]+'~'+copy[j+1:]
			j=j+1
		i=i+1	
	return ret		
				
def jaro(s1, s2):
	halflen = min(len(s1), len(s2))/2 # + min(len(s1), len(s2))%2
	com1 = getCommonCharacters(s1, s2, halflen)
	com2 = getCommonCharacters(s2, s1, halflen)
	if not len(com1) or not len(com2) : return 0.0
#	if len(com1) != len(com2) : return 0.0
	small = com1; big=com2
	if len(com1) != len(com2) :
		if len(com1) > len(com2) :
			small = com2; big=com1
	transpositions = 0
	i=0
	for ch in small :
		if ch != big[i] : transpositions = transpositions + 1
		i = i+1
	trans = (float)(transpositions) / 2 	
	finalscore = ((float)(len(com1))/len(s1) + (float)(len(com2))/len(s2) + (float)(len(com1) - trans)/len(com1)) / 3
	return finalscore


def jarowinkler(s1, s2):
	d_j = jaro(s1, s2)
	if (d_j < 0.01) : return 0.0
	l = winkler_l(s1,s2)
	return d_j + (l * 0.1 * (1 - d_j))

def getSimilarity(s1,s2):
	if s1:
		s1 = s1.lower().strip()
	if s2:
		s2 = s2.lower().strip()
	return jaro(s1,s2) if " " in s1 or " " in s2 or "." in s1 or "." in s2 else jarowinkler(s1,s2) 

def isSimilar(s1, s2, threshold=0.9):
	return getSimilarity(s1,s2) >= threshold
	
	