import sys
import os
import random

def strxor(a, b):     # xor two strings of different lengths
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def xorb(a,b):	#xor raw bytes outputs raw bytes
	return bytes(x^y for x,y in zip(a,b))

def ps3():
	x1 = '20000000000000000000000000000000'
	x2 = '30000000000000000000000000000000'

	cip2 = '9b9af18901273e33b99c3338de77b0a6'

	cip = '4f2584f0453f32f615c9afb7446b16f5'
	H =  strxor(cip.decode('hex'), cip2.decode('hex')).encode('hex')
	print H
	print strxor(H.decode('hex'), x2.decode('hex')).encode('hex')

def main():
	plaintext="P a y   B o b   1 0 0 $ " 
	cipher =  'ac1e37bfb15599e5f40eef805488281d'
	iv =      '20814804c1767293b99f1d9cab3bc3e7'
	pad1 =    '00000000000000000100000000000000'
	pad2 =    '00000000000000000500000000000000'
	print pad1[17],pad2[17]
	print iv
	pad = strxor(pad1.decode('hex'),pad2.decode('hex'))
	pad.encode('hex') == '00000000000000000400000000000000'
	t = strxor(iv.decode('hex'), pad).encode('hex')
	assert( '20814804c1767293bd9f1d9cab3bc3e7' == t)
	print t

main()
