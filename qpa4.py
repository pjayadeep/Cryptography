import urllib2
import sys
import time
from threading import Thread
from contextlib import contextmanager
#from concurrent.futures import ThreadPoolExecutor

TARGET = 'http://crypto-class.appspot.com/po?er='
glst = b' etaonhisrdluwmycgf,bp.vk"I\'-T;HMWA_SB?x!jEzCqLDYJNO:PRGFKVUXQ()0*128453679Z[]/$@&#%+<=>\\^`{|}~\x02\x03'
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------

class PaddingOracle(object):
	def __init__(self,cipher):
		self.blocks = len(cipher)/32
		self.results = [' ']*self.blocks
		# separate the blocks
		self.c = [' ']*self.blocks
		for block in range(self.blocks):
			self.c[block] = cipher[(block)*32: (block+1)*32]

	def strxor(self,a,b):
		return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a,b)])

	def oracle(self, q):
		target = TARGET + urllib2.quote(q)    # Create query URL
		req = urllib2.Request(target)         # Send HTTP request to server
		try:
			f = urllib2.urlopen(req)          # Wait for response
		except urllib2.HTTPError as e:          
			#print "We got: %d" % e.code       # Print response code
			if e.code == 404:
				return True # good padding
			return False # bad padding

	def padlength(self,c0,c1):
		altered =  c0.decode('hex')
		for i in range(1,17):
			cip = (i*'\xff' + altered[i:]).encode('hex')
			if not self.oracle(cip + c1):
				return 17-i
		return 0

	def plaintext(self, c0, c1,index, chlist=''):
		for count in range(len(chlist)+1,17):
			for ch in glst:
				pad = (16-count)*chr(0x0) + count*chr(count)
				guess = (16-count)*chr(0x0) + ch + chlist
				xorch = self.strxor(pad,guess)
				cip = self.strxor(xorch,c0.decode('hex')).encode('hex')
				if self.oracle(cip+c1):
					chlist = ch + chlist
					break
		self.results[index] = chlist
		return chlist

	def getargs(self,c,blocks):
		padlen = self.padlength(c[blocks-2],c[blocks-1])
		# for the last couple blocks
		args = [(c[blocks-2],c[blocks-1],blocks-2,padlen*chr(padlen))]
		# for the rest 
		args = args + [(c[block],c[block+1],block) for block in range(blocks-2)]
		return args

	"""
	def runinthreadpool(self,work,param):
		with concurrent.futures.ThreadPoolExecutor(max_workers=len(param)) as executor:
			futs = [executor.submit(work,arg,60) for arg in params]

			for future in concurrent.futures.as_completed(futs):
				try:
					data = future.result()
				except Exception as exc:
					print('%r generated an exception: %s') % exc
				else:
					print data
	
	"""

	def runinthreads(self,work,param):
		threads = [Thread(target=work, args=arg) for arg in param]
		for t in threads:
			t.start() 
		for t in threads:
			t.join() 

	def runserially(self,work,args):
		for arg in args:
			work(*arg) 

	def run(self):
		# Generate the arguments in args
		args = self.getargs(self.c,self.blocks)
		self.runinthreads(self.plaintext,args)
		return ''.join(self.results)

@contextmanager
def timethis(label):
	start = time.time()
	try:
		yield
	finally:
		end = time.time()
		print '%s: %0.3f' % (label, end-start)

if __name__ == "__main__":
	cip1 = ('f20bdba6ff29eed7b046d1df9fb700005'
			'8b1ffb4210a580f748b4ac714c001bd4a'
			'61044426fb515dad3f21f18aa577c0bdf'
			'302936266926ff37dbf7035d5eeb4')
	cip2 = (
    'ca0dc44d1671306407efd34b64f196bc'
    '001fbe0af1df90238429e2432db9c62d'
    'f782ffddfcf6cbd6e48241873c18ebab'
    'd3cdc510ebbe89d80b6d64c33e2ef967'
    'aaf840109065b4fcdab0dab4acb49df0'
    '04abeb0188e6ea3a5dc5d10061c074e5'
    '1a221986f547d801b2ec0239b065cd63'
    'eb78908c18cbd426ac93ea68170b0617'
    '6fe040c56e18cac659c2f649fdfb206b'
    'c45b0272165760bdac3421d847d2b70f'
    'badb01badb01badb01badb01badb01ba')

	cip3=("6569e5674cc1838d7278391a602b1b198bfa0deaeaa0ebba827172c58c6e4bbc"
           "9444efbae4c23e5f3e210d60029cecbe215df3ba44760c94dc47b2e460f0c0ed"
           "23b54c3d7b4f1d142a6bca6db6cfd438c0ffeeface0ffdec0dedbadcaca0beef")

	for cip in (cip1,cip2,cip3):
		with timethis('Time'):
			print PaddingOracle(cip).run()
