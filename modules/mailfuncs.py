import email
import base64
import quopri
from email.header import decode_header
import re

def cleanHeaderValue(value):
    
    result = re.sub(r"(=\?.*\?=)(?!$)", r"\1 ", value)
    
    if ('=?utf-8?b?' in result.lower()):
        result = result[10:]
    elif('=?windows-1251?b?' in result.lower()):
        result = result[17:]
    return result

    

def decodeHeaderValue(value):
    
    result = ''
    
    pieces = value.split()
    
    for piece in pieces:
        if ('=?utf-8?b?' in piece.lower()):
            result = result + base64.b64decode(cleanHeaderValue(piece)).decode('utf-8') + ' '
        elif ('=?windows-1251?b?' in piece.lower()):
            result = result + base64.b64decode(cleanHeaderValue(piece)).decode('windows-1251') + ' '            
        elif ('=?utf-8?q?' in piece.lower()):
            result = result + quopri.decodestring(piece.encode('utf-8')).decode('utf-8') + ' '

            
        else:
            result = result + piece + ' '
        
    return result


def decodeHeader(value):
    
    header_value = re.sub(r"(=\?.*\?=)(?!$)", r"\1 ", value)
    dh = decode_header(header_value)
    default_charset = 'utf-8'
    
    return ''.join([ str(t[0], t[1] or default_charset) for t in dh ])