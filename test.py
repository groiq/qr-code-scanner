from base45 import b45decode
from cose.messages import CoseMessage
from pprint import pprint

import zlib
import cbor2
import json

def main():
    with open('resources/vaccinationCodes.json', 'r', encoding='UTF-8') as infile:
        vaccinationCodes = json.load(infile)
    # pprint(vaccinationCodes)

    for code in readCodesFromFile('./samples/sampleQRCodes.txt'):
        rawData = decodeQR(code)
        # pprint(rawData)

        extractedData = extractRelevantJsonFields(rawData, vaccinationCodes)
        pprint(extractedData)

def readCodesFromFile(path):
    with open(path, 'r', encoding='UTF-8') as infile:
        for line in infile:
            if not line:
                continue
            yield line.rstrip().encode()

def decodeQR(input):
    left, right = input[:4], input[4:]
    if left != b'HC1:':
        raise ValueError(f'malformed prefix: should be "HC1:", but is "{left}"')

    processed = b45decode(right)
    processed = zlib.decompress(processed)
    processed = CoseMessage.decode(processed)
    return cbor2.loads(processed.payload)

def extractRelevantJsonFields(rawData, vaccinationCodes):
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
