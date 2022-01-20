from products.models import MongoProduct


def run():
    row = {
        'name': '아디다스 슈퍼스타',
        'price': 79000
    }

    # product = MongoProduct()
    # product.create(**row)

    # product = MongoProduct()
    # product.get('61e1b45112d0f2f92da4a345')
    # product.price = 10000
    # product.save()

    # product = MongoProduct('61e1b7e851375551848949eb')
    # product.price = 21000
    # product.save()

    products = MongoProduct()
    # for r in products.find():
    #     print(r)

    # for r in products.find({'name': 'test'}):
    #     print(r)

    # price >= 10000 and price <= 20000
    # for r in products.find({'price': {'$gte': 10000, '$lte': 20000}}):
    #     print(r)

    # price >= 10000 and price < 20000
    # for r in products.find({'price': {'$gte': 10000, '$lt': 20000}}):
    #     print(r)