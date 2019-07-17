from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Order(Base):
	__tablename__ = 'order'
	order_id = Column(Integer, primary_key=True)
	customer_id = Column(Integer,ForeignKey('customer.customer_id'))
	message_id = Column(Integer)
	order_datetime = Column(DateTime)    
	order_price = Column(Integer)
	
	orderproducts = relationship('OrderProduct')
    
    
class Customer(Base):
    __tablename__ = 'customer'
    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    customer_phone = Column(String)
    customer_email = Column(String)
    customer_city = Column(String)
    customer_address = Column(String)

    
class Product(Base):
    __tablename__ = 'product'
    product_id = Column(Integer, primary_key=True)
    productcategory_id = Column(Integer,ForeignKey('productcategory.productcategory_id'))
    product_title = Column(String)

    
class OrderProduct(Base):
    __tablename__ = 'orderproduct'
    orderproduct_id = Column(Integer,primary_key=True)
    order_id = Column(Integer,ForeignKey('order.order_id'))
    product_id = Column(Integer,ForeignKey('product.product_id'))
    product_price = Column(Integer)

    order = relationship('Order')
    product = relationship('Product')

    
class ProductCategory(Base):
    __tablename__ = 'productcategory'
    productcategory_id = Column(Integer, primary_key=True)
    productcategory_title = Column(String)

    
class Unit(Base):
    __tablename__ = 'unit'
    unit_id = Column(Integer, primary_key=True)
    unitcategory_id = Column(Integer,ForeignKey('unitcategory.unitcategory_id'))
    unit_title = Column(String)

    
class UnitCategory(Base):
    __tablename__ = 'unitcategory'
    unitcategory_id = Column(Integer, primary_key=True)
    unitcategory_title = Column(String)

    
class UnitProduct(Base):
    __tablename__ = 'unitproduct'
    unitproduct_id = Column(Integer,primary_key=True)
    unit_id = Column(Integer,ForeignKey('unit.unit_id'))
    product_id = Column(Integer,ForeignKey('product.product_id'))


