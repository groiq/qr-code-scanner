
# import 'python-base45'
from base45 import b45decode, b45encode

import zlib

from cose.messages import CoseMessage

import cbor2

from pprint import pprint


print('yo')

input = b'HC1:6BFNX1:HM*I0PS3TLU.NGMU5AG8JKM:SF9VN1RFBIKJ:3AXL1RR+ 8::N$OAG+RC4NKT1:P4.33GH40HD*98UIHJIDB 4N*2R7C*MCV+1AY3:YP*YVNUHC.G-NFPIR6UBRRQL9K5%L4.Q*4986NBHP95R*QFLNUDTQH-GYRN2FMGO73ZG6ZTJZC:$0$MTZUF2A81R9NEBTU2Y437XCI9DU 4S3N%JRP:HPE3$ 435QJ+UJVGYLJIMPI%2+YSUXHB42VE5M44%IJLX0SYI7BU+EGCSHG:AQ+58CEN RAXI:D53H8EA0+WAI9M8JC0D0S%8PO00DJAPE3 GZZB:X85Y8345MOLUZ3+HT0TRS76MW2O.0CGL EQ5AI.XM5 01LCWBA.RE.-SUYH+S7SBE0%B-KT+YSMFCLTQQQ6LEHG.P46UNL6DA2C$AF-SQ00A58HYO5:M8 7S$ULGC-IP49MZCSU8ST3HDRJNPV3UJADJ9BVV:7K13B4WQ+DCTEG4V8OT09797FZMQ3/A7DU0.3D148IDZ%UDR9CYF'

input = input.lstrip(b'HC1:')
# print(input)

decoded = b45decode(input)



# print(decoded)

decompressed = zlib.decompress(decoded)

decompressed = CoseMessage.decode(decompressed)

decompressed = cbor2.loads(decompressed.payload)

print(decompressed)

pprint(decompressed)

# input = "Hello world"

# toBytes = input.encode('ascii')
# b45bytes = b45encode(toBytes)
# decoded = b45bytes.b45decode('ascii')

# print(decoded)


# print(input)

# print('xx')



# output = b45decode(input)

# print(output)



print('done')