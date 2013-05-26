# South

## Primeros pasos
Vamos a dar por supuesto, siendo además nuestro caso, que el desarrollo que
estamos haciendo, lo hacemos desde 0. A partir de esta presunción, estos
serían los pasos a dar:

 * Cuando tengamos personalizado el entorno inicial, ejecutamos **manage.py syncdb** como lo hacemos normalmente

```sh
$ python manage.py syncdb
```


 1. ahora comenzaremos a crear las __apps__ que formarán el proyecto. Cuando creemos una nueva __app__, lo primero que vamos a hacer es ejecutar, después de adaptar el models.py, los siguientes comandos:
```sh
$ python manage.py schemamigration {app_name} --initial
```
Ahora hacemos la migración en si:
```sh
$ python manage.py migrate {app_name}
```
Esto se hace solo la primera vez, la inicial


 2. A partir de aquí, cada vez que se ejecute un cambio en el models.py de esa misma aplicación, se ejecutarán estos dos pasos:
```sh
$ python manage.py schemamigration {app_name} --auto
$ python manage.py migrate {app_name}
```

## Otros comandos útiles

 * Test del esquema de migración generado:
```sh
$ python manage.py schemamigration {app_name} --auto --stdout
```

 * Migración de pruebas (no toca la BBDD)
```sh
$ python manage.py migrate myapp --db-dry-run
```

 * Listar las migraciones almacenadas:
```sh
$ python manage.py migrate --list
```

 * Borrar las migraciones realizadas:
Algunas veces, tenemos que resetear el control de migraciones a 0. Este comando borrará toda la historia de migraciones de la BBDD, pero dejará los ficheros models.py intectos.
```sh
$ python manage.py migrate {app_name} zero
```

# Referencias
 * http://unoyunodiez.com/2011/05/03/django-en-cero-coma-i/
 * http://unoyunodiez.com/2011/05/03/django-en-cero-coma-ii/

 * http://conocimientoabierto.es/tutorial-basico-django-south/493/

 * http://pablogplanet.blogspot.com.es/2010/06/notas-mini-tutorial-django-south.html

 * http://pablogplanet.blogspot.com/2010/07/nota-anadiendo-south-un-projecto.html

 * http://www.djangopro.com/2011/01/django-database-migration-tool-south-explained/

# Notas sobre Django 1.5:
 * http://unoyunodiez.com/2013/03/16/django-in-a-nutshell-i/
 * http://unoyunodiez.com/2013/04/04/django-in-a-nutshell-ii/
