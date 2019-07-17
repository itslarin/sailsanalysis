from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import dbstruct
import messagestruct
 
 
   
def dbGetEngine(host,port,database,user,password):
    #return create_engine('postgresql+psycopg2://weukgmth:EjnV3ZckgHVsF9P8uTRO-WkmESwBTzOB@manny.db.elephantsql.com:5432/weukgmth')    
    #return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")    
	return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}",pool_size=1, max_overflow=0)    
    
    
	
def dbGetSession(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


	
def submitMessage(session,message):
	
	session.merge(dbstruct.Customer(customer_id=message.customer['customerId'],customer_name=message.customer['customerName'],customer_phone=message.customer['customerPhone'],customer_email=message.customer['customerEmail'],customer_city=message.customer['customerCity'],customer_address=message.customer['customerAddress']))


	session.merge(dbstruct.Order(order_id=message.order['orderId'],customer_id=message.customer['customerId'],message_id=message.order['messageId'],order_datetime=message.order['orderDateTime'],order_price=message.order['orderPrice']))
	
	
	for product in message.products:
	
		session.merge(dbstruct.ProductCategory(productcategory_id=product['productCategoryId'],productcategory_title=str(product['productCategoryId'])))
	
		session.merge(dbstruct.Product(product_id=product['productId'],productcategory_id=product['productCategoryId'],product_title=product['productTitle']))
	
	
		for i in range(0,product['productQuantity']):
			
			session.merge(dbstruct.OrderProduct(orderproduct_id=int(str(message.order['orderId']) + str(i)),order_id=message.order['orderId'],product_id=product['productId'],product_price=product['productPrice']))
	

