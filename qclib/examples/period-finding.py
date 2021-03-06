#!/usr/bin/python

import qclib
import numpy as np
from fractions import gcd

# Initialize the Quantum Computer
nqbits = 8 # per the definition of f(x) below, must be >= 4
q = qclib.qcsim(nqbits)

M = 2**(nqbits-2)

# setup the periodic function
op1 = q.qstretch(q.C(),[2,0])
op2 = q.qstretch(q.C(),[3,1])
f = q.qcombine_seq("F(x)",[op1,op2])
print "Psst ... f(x) defined as having period of 4\n"

# Now loop to repeatedly find values of multiples of M/r by
# running the QC repeatedly and reading the outputs
idx = 0
vals = np.zeros(2)
while idx < 2:
	# Restart the QC machine
	q.qreset()

	# QFT(x) - F(x) - QFT(x) - Measure
	q.qgate(q.QFT(nqbits-2),range(nqbits-1,1,-1))
	q.qgate(f,list(reversed(range(nqbits))))
	# measure this if you like - q.qmeasure([1,0])
	q.qgate(q.QFT(nqbits-2),range(nqbits-1,1,-1))
	mbyrarr = q.qmeasure(range(nqbits-1,1,-1))

	# convert to integer the measured values of the x register
	mbyr = 0
	for i in range(nqbits-2):
		sign = nqbits-2-1-i
		if mbyrarr[i] == 1:
			mbyr += 2**sign

	# Look for two distinc non-zero values
	print "a multiple of M/r = ",mbyr
	if mbyr != 0:
		vals[idx] = mbyr
		if (vals[0] != vals[1]):
			idx += 1

# find the GCD of the two values read to get M/r, and compute r, as M is known
mbyr = int(gcd(vals[0], vals[1]))
print "GCD of values of M/r = {:d}\n".format(mbyr)
print "But, M =", M
r = int(M / mbyr)
print "Therefore, the period, r = ",r
