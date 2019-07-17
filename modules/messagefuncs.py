import email
import base64
import quopri
from email.header import decode_header
import re
import messagestruct
from bs4 import BeautifulSoup
import time
import datetime



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
	
	
def parseMessage(messageId,message):
	
	messageDate = message["Date"]
	messageSubject = decodeHeader(message["Subject"])
	messageBody = message.get_payload()
		
	parsedMessageBody = BeautifulSoup(messageBody, 'html.parser')
	
	
	#order section
	orderId = int(messageSubject.split()[1].strip(','))
	orderDateTime = datetime.datetime.fromtimestamp(time.mktime(email.utils.parsedate(messageDate)))
	orderPrice = int(float((messageSubject.split()[-2]).replace(',','.')))
	messageId = int(messageId)
	
	order = {
		"orderId": orderId,
		"orderDateTime": orderDateTime,
		"orderPrice": orderPrice,
		"messageId": messageId
	}
	#order section end
	
	
	#customer section
	customerName = parsedMessageBody.find('span', class_='vm2-last_name').text if parsedMessageBody.find('span', class_='vm2-last_name') is not None else ""
	customerPhone = parsedMessageBody.find('span', class_='vm2-phone_1').text if parsedMessageBody.find('span', class_='vm2-phone_1') is not None else ""
	customerEmail = parsedMessageBody.find('span', class_='vm2-email').text if parsedMessageBody.find('span', class_='vm2-email') is not None else ""
	customerCity = parsedMessageBody.find('span', class_='vm2-virtuemart_state_id').text if parsedMessageBody.find('span', class_='vm2-virtuemart_state_id') is not None else ""
	customerAddress = parsedMessageBody.find('span', class_='vm2-address_1').text if parsedMessageBody.find('span', class_='vm2-address_1') is not None else ""
	
	
	customer = {		
		"customerId": orderId,
		"customerName": customerName,
		"customerPhone": customerPhone,
		"customerEmail": customerEmail,
		"customerCity": customerCity,
		"customerAddress": customerAddress
	}
	#customer section end
	
	
	#products section
	products = []
	
	productTable = parsedMessageBody.find('tr', class_='sectiontableheader').parent
	productRows = productTable.find_all('tr')[1:-5]	
	
	
	for productRow in productRows:
		
		productCells = productRow.find_all('td')

		productHref = productCells[1].find('a', href=True)
		productId = int(productHref['href'].split('&')[-2].split('=')[1])
		productCategoryId = int(productHref['href'].split('&')[-3].split('=')[1])
		productTitle = productHref.text
		productPrice = int(float((productCells[2].text.split()[0]).replace(',','.')))
		productQuantity = int(productCells[3].text)

		product = {
			"productId": productId,
			"productCategoryId": productCategoryId,
			"productTitle": productTitle,
			"productPrice": productPrice,
			"productQuantity": productQuantity		
		}
	
		products.append(product)
		
	
	#products section end
	
	
	return messagestruct.Message(order, customer, products)