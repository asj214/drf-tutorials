from __future__ import absolute_import
from conf.celery import app


@app.task(ignore_result=False)
def add(x, y):
    return x + y