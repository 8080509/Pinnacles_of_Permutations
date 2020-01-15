
from itertools import chain, repeat

def factorial(n):
	"""Returns n! for a non-negative integer n."""
	acc = 1
	for i in range(1, n+1):
		acc *= i
	return acc

def serialize(mapping):
	"""Computes a unique numerical representation of a permutation.
	
	Note that permutations are expected to contain only elements from range(0, n), where n is the length of the permutation.
	
	Returns (number, size):
		'number' is the serialized representation, and lies in range(0, factorial(size)).
		'size' is the length of the permutation.
	
	The function 'deserialize' performs the reverse operation.
	"""
	ops = list(range(len(mapping)))
	nums = []
	for e in mapping:
		i = ops.index(e)
		del ops[i]
		nums.append(i)
	number = 0
	size = 0
	for i in nums[::-1]:
		size += 1
		number *= size
		number += i
	return (number, size)

def deserialize(number, size):
	"""Given a numerical representation of a permutation, returns said permutation.
	
	Every number in range(0, factorial(size)) returns a distinct permutation of length 'size'.
	Reverse of 'serialize'.
	
	deserialize(*serialize(x)) == x
	"""
	ops = list(range(size))
	mapping = []
	while size:
		(number, x) = divmod(number, size)
		mapping.append(ops.pop(x))
		size -= 1
	return mapping

def getPV(x):
	"""Returns the pinnacle and vale set of the given permutation."""
	edge = float('inf')
	x = [*x]
	x.append(edge)
	P = set()
	V = set()
	preV = x.pop(0)
	preD = True
	for j in x:
		newD = preV > j
		if (not preD) and newD:
			P.add(preV)
		elif preD and (not newD):
			V.add(preV)
		preV = j
		preD = newD
	return P, V

def pin(x):
	"""Returns the pinnacle set of the given permutation."""
	return getPV(x)[0]

def vale(x):
	return getPV(x)[1]

def pinGen1(n, pins):
	"""Returns permutations from Sn with pinnacle set 'pins'.
	
	Note that 'pins' must be a set of integers for correct behavior.
	
	This method is the naive pinnacle generation implementation.  Simply generates all n! permutations in Sn, and yields only those with the correct pinnacle set.
	"""
	for i in range(factorial(n)):
		x = deserialize(i,n)
		if pin(x) == pins: yield x

def altPinGen1(n, pins):
	"""Alternative implementation of the naive algorithm in 'pinGen1'."""
	return filter(
		lambda i: pin(i) == pins,
		map(
			deserialize,
			range(factorial(n)),
			repeat(n)
		)
	)

def pinGen2(n, pins):
	"""Returns permutations from Sn with pinnacle set 'pins'.
	
	The method uses the new implementation described in the paper.
	"""
	#The method is broken into several iterators.  This is the highest level.
	#This one calls newFSPRootGen to produce the cannonical representatives, and feeds them through newFSOrbitIter to cycle through all the elements in the same orbit under the Foata-Strehl action.
	return chain.from_iterable(map(newFSOrbitIter, newFSPRootGen(sorted(pins), n)))

def newFSOrbitIter(m):
	"""Generates all permutations in the same Foata-Strehl orbit of the given pinnacle."""
	out = [m]
	V = vale(m)
	for x in filter(lambda i: i not in V, range(len(m))):
		new = [fSActionX(m, x) for m in out]
		out.extend(new)
	return out

def fSActionX(m,x):
	"""Performs the elementary operation in the Foata-Strehl action."""
	(w1,w2,w4,w5) = xFactor(m,x)
	return [*w1,*w4,x,*w2,*w5]

def xFactor(m,x):
	"""Partitions m according to the x-factorization described in the paper."""
	j = m.index(x)
	i = j-1
	while i >= 0 and m[i] < x: i -= 1
	i+=1
	w1 = m[:i]
	w2 = m[i:j]
	j += 1
	i = j
	n = len(m)
	while i < n and m[i] < x: i += 1
	w4 = m[j:i]
	w5 = m[i:]
	return (w1,w2,w4,w5)

def newFSPRootGen(pins, n):
	"""Generates all the canonical representatives in Sn with the given pinnacle set."""
	#Does so by generating all canonical arrangments with newFullArrGen, and adding the ascending values using newPinPopulate.
	return chain.from_iterable(newPinPopulate(a, pins, n) for a in newFullArrGen(pins))

def newPinPopulate(l, tPins, ops):
	"""Given a canonical arrangment, pinnacle set, and n, yields all canonical representatives corresponding to the arrangment."""
	if isinstance(ops, int):
		ops = list(range(ops))
		if not l: yield ops; return
		for i in l: ops.remove(i)
	else:
		ops = ops.copy()
	if not ops:
		yield l
		return
	i = ops.pop(0)
	pins = tPins.copy()
	for j in tPins:
		if i > j: pins.remove(j)
	ln = len(l)
	for k in range(1, ln+1):
		if (((k != ln) and (l[k] not in pins))) or (l[k-1] > i): continue
		m = l.copy()
		m.insert(k, i)
		for r in newPinPopulate(m, pins, ops): yield r

def newFullArrGen(pins):
	"""Generates all arrangments with the given pinnacle set."""
	#Does so by taking all admissible vale sets from valeSetGenF, and producing all PV-arrangments using arrGen
	return chain.from_iterable(map(arrGen, repeat(pins), valeSetGenF(pins)))

def arrGen(P,V):  #Let P and V be sorted lists
	"""Generates all PV-arrangments, given P and V."""
	#Does so using the recursive method described in the paper.
	if len(P) == 0: yield V; return
	if len(P) == 1: [v1,v2] = V; yield [v1,*P,v2]; return #This is for optimization.
	P = P.copy()
	p = P.pop(0)#P is now P', stored under the same variable for efficiency
	V1 = list(filter(lambda i: i < p, V)) #this is Vp from the notes
	V2 = V.copy() #this is just for optimization
	V2.insert(V.index(max(V1)) + 1, p)
	for [v1,v2] in subsetIter(V1, 2):
		V3 = V2.copy() #this will be V' from the notes
		V3.remove(v1)
		V3.remove(v2)
		for a in arrGen(P,V3): #here a' is selected
			j = a.index(p)
			a.insert(j+1,v2) #this line, and the following produce a, corresponding to a'.
			a.insert(j,v1)
			yield a

def subsetIter(coll, k):
	"""Iterates through the 'k'-element subsets of 'coll'."""
	if k == 0: yield []; return
	tCol = coll.copy()
	for _ in range(k-1, len(tCol)):
		x = tCol.pop()
		for i in subsetIter(tCol, k-1): i.append(x); yield i

def valeSetGenF(P):
	"""Given a pinnacle set, generates all admissible vale sets."""
	#Does so by (after checking for the trival case) invoking valeSetGenFSub
	P = sorted(P)
	if not P:
		return ([0],)
	return valeSetGenFSub(P, set(P))

def valeSetGenFSub(P, pSet = None):
	"""Recursive component of valeSetGenF."""
	#Essentially, this function works by adding vales in descending order.
	#For a pinnacle set P = [p1 < p2 < ... < pk], generates all vale sets V = [0 = v0 < v1 < v2 < ... < vk], with the condition that (vi < pi) and (vi not in pSet) for all i from 1 to k.
	pm = P.pop(0)
	if not P:
		for v in filter(lambda i : i not in pSet, range(1, pm)):
			yield [0, v]
		return
	for V in valeSetGenFSub(P, pSet):
		for v in filter(lambda i : i not in pSet, range(1, min(pm, V[1]))):
			nV = V.copy()
			nV.insert(1, v)
			yield nV







































