from hashlib import sha256

fd,h = open('pa3-file3.mp4','rb') ,''
for block in reversed(list(iter(lambda:fd.read(1024), ''))):
	h = sha256(block+h).digest()

print h.encode('hex')
