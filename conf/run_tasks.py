import time
from .tasks import add


if __name__ == '__main__':
    result = add.delay(1, 2)
    print('Task finished? ', result.ready())
    print('Task result: ', result.result)

    while not result.ready():
        time.sleep(1)

    print('Task finished? ', result.ready())
    print('Task result: ', result.result)
