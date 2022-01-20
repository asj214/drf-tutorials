### drf-tutorials

```sh
python -m venv .venv

. .venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

# fixture
sh init.sh

python manage.py runserver
```


### fixture
```sh
# dumps
python manage.py dumpdata users.User --format=yaml > scripts/fixtures/users.yaml

# loads
python manage.py loaddata scripts/fixtures/users.yaml
```

### celery
```sh
celery -A conf worker -P solo --loglevel=info
celery -A conf worker -P solo --loglevel=debug
celery -A conf flower

python -m conf.run_tasks
```
