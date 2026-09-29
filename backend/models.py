from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.sql import func
from backend.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20))
    language = Column(String(50), default="English")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String(150), nullable=False)
    owner_name = Column(String(100))
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20))
    location = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)
    property_type = Column(String(100), nullable=False)
    length = Column(String(50))
    width = Column(String(50))
    location = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PropertyImage(Base):
    __tablename__ = "property_images"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Design(Base):
    __tablename__ = "designs"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, nullable=False)
    option_number = Column(Integer, nullable=False)
    prompt = Column(Text)
    image_url = Column(String(1000), nullable=False)
    selected = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DesignCustomization(Base):
    __tablename__ = "design_customizations"

    id = Column(Integer, primary_key=True, index=True)
    design_id = Column(Integer, nullable=False)
    room = Column(String(100))
    customization_request = Column(Text, nullable=False)
    parsed_result = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(Integer, nullable=False)
    product_name = Column(String(200), nullable=False)
    category = Column(String(100))
    description = Column(Text)
    price = Column(Float)
    stock = Column(Integer, default=0)
    image_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Negotiation(Base):
    __tablename__ = "negotiations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    client_id = Column(Integer, nullable=False)
    merchant_id = Column(Integer, nullable=False)
    offered_price = Column(Float)
    status = Column(String(50), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())