from django.db import transaction
from shops.models import Shop
from products.models import Product


def run():
    shops = Shop.objects.active().all()
    with transaction.atomic():
        for r in Product.objects.all():
            for shop in shops:
                r.shops.create(
                    code=shop.code,
                    value=r.name,
                    is_sale_period=r.is_sale_period,
                    price=r.price,
                    started_at=r.started_at,
                    finished_at=r.finished_at,
                )
            r.save()
