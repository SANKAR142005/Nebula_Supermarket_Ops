from datetime import datetime, timezone
from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey,Text,UniqueConstraint
from sqlalchemy.orm import relationship
from app.storage.connection import Base

def now(): return datetime.now(timezone.utc).replace(tzinfo=None)

class Product(Base):
    __tablename__='products'
    id=Column(Integer,primary_key=True)
    name=Column(String(120),nullable=False)
    sku=Column(String(50),unique=True,nullable=False)
    unit=Column(String(20),default='pcs')
    sell_price=Column(Float,nullable=False,default=0)
    cost_price=Column(Float,nullable=False,default=0)
    mrp=Column(Float,nullable=False,default=0)
    quantity=Column(Float,nullable=False,default=0)
    reorder_point=Column(Float,nullable=False,default=5)
    gst_rate=Column(Float,default=0)
    hsn=Column(String(30))
    expiry_date=Column(String(20))

class Client(Base):
    __tablename__='clients'
    id=Column(Integer,primary_key=True)
    name=Column(String(120),nullable=False)
    phone=Column(String(30),unique=True)
    credit_due=Column(Float,default=0)

class Sale(Base):
    __tablename__='sales'
    id=Column(Integer,primary_key=True)
    status=Column(String(20),default='open')
    client_id=Column(Integer,ForeignKey('clients.id'))
    subtotal=Column(Float,default=0)
    tax=Column(Float,default=0)
    total=Column(Float,default=0)
    payment=Column(String(20))
    created_at=Column(DateTime,default=now)
    client=relationship('Client')
    lines=relationship('SaleLine',back_populates='sale',cascade='all, delete-orphan')

class SaleLine(Base):
    __tablename__='sale_lines'
    id=Column(Integer,primary_key=True)
    sale_id=Column(Integer,ForeignKey('sales.id'),nullable=False)
    product_id=Column(Integer,ForeignKey('products.id'),nullable=False)
    quantity=Column(Float,nullable=False)
    unit_price=Column(Float,nullable=False)
    tax=Column(Float,default=0)
    sale=relationship('Sale',back_populates='lines')
    product=relationship('Product')

class UserSetting(Base):
    __tablename__='user_settings'
    id=Column(Integer,primary_key=True)
    key=Column(String(60),unique=True,nullable=False)
    value=Column(Text,nullable=False)

class ChatState(Base):
    __tablename__='chat_states'
    id=Column(Integer,primary_key=True)
    channel_id=Column(String(80),unique=True,nullable=False)
    transcript=Column(Text,default='[]')
