import sqlalchemy as sq
import sqlalchemy.orm
import task1
import json

# --------------- ЗАДАНИЕ 3 ---------------
# ----- Информация о БД -----
bd = 'postgresql'
login = 'postgres'
password = '1234'
name_bd = 'test1'

# ----- Настройка движка и создание сессии -----
puthDB = f"{bd}://{login}:{password}@localhost:5432/{name_bd}"
engine = sq.create_engine(puthDB)
session = sqlalchemy.orm.sessionmaker(engine)()

# ----- Пересоздание таблиц (при их наличии) -----
task1.basic.metadata.drop_all(engine)
task1.basic.metadata.create_all(engine)

# ----- Наполнение таблиц (из JSON файла) -----
dict_models = {'publisher': task1.Publisher,
               'book': task1.Book,
               'shop': task1.Shop,
               'stock': task1.Stock,
               'sale': task1.Sale}
with open('fictures/data_models.json', encoding='utf-8') as f:
    reader = json.load(f)
    for el in reader:
        session.add(dict_models[el['model']](**el['fields']))

# --------------- ЗАДАНИЕ 2 ---------------

info = input('Введите имя или id автора: ')
info_ = (task1.Publisher.id, int(info)) if info.isdigit() else (task1.Publisher.name, info)

book_, store_, price_, date = [], [], [], []
for pub in session.query(task1.Publisher).filter(info_[0] == info_[1]):
    for book in pub.publishes:
        for stock in book.books:
            for sale in stock.stocks:
                store = session.query(task1.Shop).filter(task1.Shop.id == stock.id_shop)[0].name.strip()
                book_.append(book.title.strip()), store_.append(store)
                price_.append(round(sale.price * sale.count, 2)), date.append(sale.date_sale)

max1, max2, max3 = (max(len(i) for i in book_),  max(len(i) for i in store_),
                          max(len(str(i)) for i in price_))

for i in range(len(book_)):
    print(f"{book_[i]:<{max1}} | {store_[i]:<{max2}} | {price_[i]:<{max3}} | {date[i].strftime('%Y-%m-%d')}")

session.commit()
session.close()
