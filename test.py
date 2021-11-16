from base45 import b45decode, b45encode
from cose.messages import CoseMessage
from pprint import pprint

import zlib
import cbor2
import json

def main():
    input = b'HC1:6BFNX1:HM*I0PS3TLU.NGMU5AG8JKM:SF9VN1RFBIKJ:3AXL1RR+ 8::N$OAG+RC4NKT1:P4.33GH40HD*98UIHJIDB 4N*2R7C*MCV+1AY3:YP*YVNUHC.G-NFPIR6UBRRQL9K5%L4.Q*4986NBHP95R*QFLNUDTQH-GYRN2FMGO73ZG6ZTJZC:$0$MTZUF2A81R9NEBTU2Y437XCI9DU 4S3N%JRP:HPE3$ 435QJ+UJVGYLJIMPI%2+YSUXHB42VE5M44%IJLX0SYI7BU+EGCSHG:AQ+58CEN RAXI:D53H8EA0+WAI9M8JC0D0S%8PO00DJAPE3 GZZB:X85Y8345MOLUZ3+HT0TRS76MW2O.0CGL EQ5AI.XM5 01LCWBA.RE.-SUYH+S7SBE0%B-KT+YSMFCLTQQQ6LEHG.P46UNL6DA2C$AF-SQ00A58HYO5:M8 7S$ULGC-IP49MZCSU8ST3HDRJNPV3UJADJ9BVV:7K13B4WQ+DCTEG4V8OT09797FZMQ3/A7DU0.3D148IDZ%UDR9CYF'

    rawData = decodeQR(input)
    # pprint(rawData)

    extractedData = extractRelevantJsonFields(rawData)
    pprint(extractedData)

def decodeQR(input):
    left, right = input[:4], input[4:]
    if left != b'HC1:':
        raise ValueError(f'malformed prefix: should be "HC1:", but is "{left}"')

    processed = b45decode(right)
    processed = zlib.decompress(processed)
    processed = CoseMessage.decode(processed)
    return cbor2.loads(processed.payload)

def extractRelevantJsonFields(rawData):
    with open('./vaccinationCodes.json', 'r', encoding='UTF-8') as infile:
        vaccinationCodes = json.load(infile)
    # pprint(vaccinationCodes)

    extractedData = {}

    vaccine = rawData[-260][1]['v'][0]
    manufacturerCode = vaccine['ma']
    extractedData['manufacturer'] = vaccinationCodes['manufacturer'].get(manufacturerCode, 'unknown')
    extractedData['vaccinationDate'] = vaccine['dt']
    extractedData['publisher'] = vaccine['is']

    patientName = rawData[-260][1]['nam']
    extractedData['firstName'] = patientName['gn']
    extractedData['lastName'] = patientName['fn']
    return extractedData

if __name__ == '__main__':
    main()
