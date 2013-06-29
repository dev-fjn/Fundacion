# Cómo gestionar las fixtures:
https://code.djangoproject.com/wiki/Fixtures

Generación de las fixtures:
```sh
./manage.py dumpdata --format=json --indent=4 myapp > myapp/fixtures/myapp.json
```

Carga manual de datos:
```sh
./manage.py loaddata myapp
```
