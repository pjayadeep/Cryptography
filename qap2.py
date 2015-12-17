def findduskcode():
	cip = '6c73d5240a948c86981bc294814d'
	key = 'c294814d'
	print (key)
	f =  strxor( key.encode('hex'),'dawn')
	print (f.encode('hex'))
	print (strxor(f,'dusk').encode('hex'))

	cipstr = '32510ba9babebbbefd001547a810e67149caee11d945cd7fc81a05e9f85aac650e9052ba6a8cd8257bf14d13e6f0a803b54fde9e77472dbff89d71b57bddef121336cb85ccb8f3315f4b52e301d16e9f52f904'
#findduskcode()

l = [("4af532671351e2e1" , "87a40cfa8dd39154"), ("7b50baab07640c3d","ac343a22cea46d60"), ("9d1a4f78cb28d863", "75e5e3ea773ec3e6"), ("290b6e3a39155d6f", "d6f491c5b645c008")]

l2 = [ ("7b50baab07640c3d","ac343a22cea46d60"),
("e86d2de2e1387ae9",    "1792d21db645c008"),
("7c2822ebfdc48bfb",    "325032a9c5e2364b"),
("2d1cfa42c0b1d266",    "eea6e3ddb2146dd0") ]

l3 = [("2d1cfa42c0b1d266",    "eea6e3ddb2146dd0"),
("9f970f4e932330e4",    "6068f0b1b645c008"),
("7b50baab07640c3d",    "ac343a22cea46d60"),
("5f67abaf5210722b",    "bbe033c00bc9330e")
]

l4 = [
("e86d2de2e1387ae9","1792d21db645c008"),
("7c2822ebfdc48bfb","325032a9c5e2364b"),
("9d1a4f78cb28d863","75e5e3ea773ec3e6"),
("5f67abaf5210722b","bbe033c00bc9330e"),
]

for a,b in l4:
	print (strxor(strtocip(a),strtocip(b)).encode('hex'))


