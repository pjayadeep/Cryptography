from numbthy import powmod,xgcd
from time import time 
from math import pow
from threading import Thread
from contextlib import contextmanager

p1=1073676287;
g1=1010343267;
h1=857348958;
B1=2**10;
Ans = 1026831

p=  13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171L
g = 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568L
h = 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333L
B = powmod(2,20,p)
#ans = 375374217830


def Dlog(g,h,p,S,B):
	hasht = {}
	gI = xgcd(g,p)[1] # inverse of g^-1, powmod(g,-1,p) returns 1??
	hx = h

	for x1 in xrange(S,B):
		hx =( hx * gI) % p  # h/g**x1
		hasht[hx] = x1

	gB = powmod(g,B,p)
	rhs = 1
	x=''
	for x0 in xrange(B):
		if hasht.has_key(rhs):
			x= x0*B + hasht[rhs]+1
			print x,x0
			assert (powmod(g,x,p) == h)
			break
		rhs = (rhs * gB) % p  # gB**x0
	return  x

@contextmanager
def timethis(label):
	start = time()
	try:
		yield
	finally:
		end = time()
		print '%s: %0.3f' % (label, end-start)


if __name__ == "__main__":
	with timethis('PA5'):
		print Dlog(g,h,p,0,B)
	with timethis('eg'):
		print Dlog(g1,h1,p1,0,B1)
