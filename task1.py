import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

basic = declarative_base()


class Publisher(basic):
    __tablename__ = 'publisher'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.CHAR(length=30), nullable=True)


class Book(basic):
    __tablename__ = 'book'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.CHAR(length=50), nullable=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=True)
    publish = relationship(Publisher, backref='publishes')


class Shop(basic):
    __tablename__ = 'shop'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.CHAR(length=50), nullable=True)


class Stock(basic):
    __tablename__ = 'stock'
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=True)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=True)
    count = sq.Column(sq.Integer, default=0, nullable=True)
    book = relationship(Book, backref='books')
    shop = relationship(Shop, backref='shops')


class Sale(basic):
    __tablename__ = 'sale'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, default=None)
    date_sale = sq.Column(sq.DateTime, default=None)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'))
    count = sq.Column(sq.Integer, default=0, nullable=True)
    stock = relationship(Stock, backref='stocks')
