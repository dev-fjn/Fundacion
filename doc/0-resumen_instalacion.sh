#!/bin/sh -x
# Se asume: python 2.7.3

# Pillar actualizaciones del repo
git pull

# Limpiar todo lo posible
#rm -Rf .gitignore static virtualenv external/*
#cp .gitignore-minimo .gitignore
#git status # ver que no hay nada "extra"
#rm -Rf seguir_Borrando_cosas_sobrantes

# Revertimos gitignore aunque yo lo borraria
#git checkout .gitignore

# Pillamos los external
git submodule update

# Vemos que ningun enlace simbolico está roto
ls -l; echo "vemos que ningun enlace simbolico esta roto, pulsa enter"; read

# Configuracion en desarrollo
cp portal/settings.d/000.STATUS.py.demo portal/settings.d/000.STATUS.py

# Generacion del virtualenv standard style
test -d virtualenv || virtualenv virtualenv
. virtualenv/bin/activate
pip install -r requirements.txt
deactivate

## Hay paquetes python compilados como python-imaging (PIL) que yo pondría de paquete debian porque te obligan a instalar un gcc y cientos de -dev en un servidor y eso no mola... además, normalmente son paquetes auxiliares que usas lo básico y no necesitas estos paquetes a la hiper-última
## (o sea, que desactivaria el --no-site-packages del virtualenv)

# Testear que está el virtualenv fino
./python.sh manage.py ; echo "Si el python manage.py fue bien, pulsamos enter"; read

# Crear base de datos (en sqlite debido a que estamos en debug!produccion)
./python.sh manage.py syncdb --noinput

# Crear base de datos #2
./python.sh manage.py migrate

# Crear /var/www/tal (realmente ./static)
./python.sh manage.py collectstatic --noinput

# Pillar menus de serie
./python.sh  manage.py loaddata fixtures/treemenus.json 

# Pillar algunas paginas de ejemplo
./python.sh manage.py loaddata fixtures/flatpages_i18n.json

# Crear usuarios administradores (pregunta passwd)
./python.sh manage.py createsuperuser --username=root --email=root@root.com 

# Arrancar
./python.sh manage.py runserver

# Mirar
# http://localhost:8000/
# http://localhost:8000/admin/
# http://localhost:8000/acercade/ (una flat page)
# http://localhost:8000/calendar/ (con plantilla pero vacia)
# http://localhost:8000/contact/ (sin plantilla)
# http://localhost:8000/plantilla/ (igual?)
# http://localhost:8000/sitemap.xml (Contenido absurdo)
# http://localhost:8000/weblog/ (plantilla diferente)
