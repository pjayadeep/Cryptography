import urllib2
import string

TARGET = 'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:          
            # print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding
        print 'url ok'

cs = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044'\
     '426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'

letters = string.ascii_lowercase+string.ascii_uppercase+' '

letters2 = b' etaonhisrdluwmycgf,bp.vk"I\'-T;HMWA_SB?x!jEzCqLDYJNO:PRGFKVUXQ'\
           '()0*128453679Z[]/$@&#%+<=>\\^`{|}~\x02\x03'

# Using a padding oracle (CBC encryption)
# 07-authenc-v2-annotated.pdf page 51
def decodePair(c1, c2, last=16):
    rl = [ord(x) for x in letters2]
    c2h = c2.encode('hex')
    pad = 16-last
    m = [0]*last + [pad]*pad
    for index in range(last-1, -1, -1):
        pad = 16-index
        pads = [0]*index+[pad]*pad
        # c1 ^ m ^ pads
        c1l = [ord(x1)^x2^x3 for x1,x2,x3 in zip(list(c1),m, pads)]     
        c1lnew = c1l[:]
        for g in rl:
            c1lnew[index]=c1l[index]^g # c1^m^pads^g
            q = ''.join([chr(x) for x in c1lnew]).encode('hex') + c2h
            if po.query(q):       
                print '%2d:%3d:%1s' %(index, g, chr(g)), q[:32]
                break
        m[index] = g
    return ''.join([chr(x) for x in m])[:last]

##def findpad(c1, c2):
##    c1l = list(c1)
##    for g in range(16, 0, -1):
##        c1l[15]=chr(ord(c1[15])^g^1)
##        q = ''.join(c1l).encode('hex') + c2.encode('hex')
##        if po.query(q):
##            return g
##    return -1

# as described by Murphy PA4: Problem/Errata in the last block
def findpadposKatz(c1, c2):
    for i in range(16):
        c1l = list(c1)
        c1l[i] = chr(ord(c1l[i])^0xFF)      # change byte
        q = ''.join(c1l).encode('hex') + c2.encode('hex')
        if not po.query(q):
            return i
    return -1


DECODE = True
# DECODE = False

if __name__ == "__main__":
    po = PaddingOracle()
    c = []
    for i in range(0, len(cs),32):
        c.append(cs[i:i+32].decode('hex'))
    if DECODE:
        m = ''
        for i in range(len(c)-2):
            m += decodePair(c[i], c[i+1])
        padpos = findpadposKatz(c[i+1],c[i+2])
        m  += decodePair(c[i+1], c[i+2], padpos)
        print m
    
