from shops.models import Shop


def run():
    rows = [
        {
            'code': 'en',
            'name': '영어',
            'order': 1,
            'is_active': True
        },
        {
            'code': 'ko',
            'name': '한글',
            'order': 2,
            'is_active': True
        }
    ]

    for row in rows:
        Shop.objects.create(**row)