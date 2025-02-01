from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    subcategories = relationship("Subcategory", back_populates="category")


class Subcategory(Base):
    __tablename__ = "subcategories"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="subcategories")
    products = relationship("Product", back_populates="subcategory")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    photo_url = Column(String)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"))
    subcategory = relationship("Subcategory", back_populates="products")


class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    product = relationship("Product")


class FAQ(Base):
    __tablename__ = "faq"
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    items = Column(String, nullable=False)  # JSON-like string of products
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
