from shops.models import Shop
from categories.models import Category


def run():
    shops = Shop.objects.active().all()

    for r in Category.objects.all():
        for shop in shops:
            r.names.create(code=shop.code, value=r.name)
        r.save()
