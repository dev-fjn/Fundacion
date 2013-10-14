#!/bin/sh -x

# Crear las carpetas para el static y el media en /var/www/fjn/

mkdir /var/www/fjn/
cd /var/www/fjn/
mkdir -p beta/static beta/media
mkdir -p dev/static dev/media
mkdir -p www/static www/media

# Crear base de datos para produccion (beta y dev no pues van con sqlite)

su - postgres
createuser fjn --no-superuser --no-createrole --no-createdb --password
createdb fjn --owner fjn
exit

# clonar cada uno de los despliegues en /opt/fjn/

mkdir -p /opt/fjn

test -d /opt/fjn/dev || git clone git@github.com:dev-fjn/Fundacion.git /opt/fjn/dev
cd /opt/fjn/dev
git checkout develop
echo "DEBUG = True" > portal/settings.d/000.STATUS.py
echo "PRODUCCION = False" >> portal/settings.d/000.STATUS.py
bash -x doc/0-resumen_instalacion.sh

test -d /opt/fjn/beta || git clone git@github.com:dev-fjn/Fundacion.git /opt/fjn/beta
cd /opt/fjn/beta
git checkout master
echo "DEBUG = True" > portal/settings.d/000.STATUS.py
echo "PRODUCCION = True" >> portal/settings.d/000.STATUS.py
bash -x doc/0-resumen_instalacion.sh

test -d /opt/fjn/www || git clone git@github.com:dev-fjn/Fundacion.git /opt/fjn/www
cd /opt/fjn/www
git checkout master
echo "DEBUG = True" > portal/settings.d/000.STATUS.py
echo "PRODUCCION = False" >> portal/settings.d/000.STATUS.py
bash -x doc/0-resumen_instalacion.sh

# Configurar el nginx

cd /etc/nginx/sites-enabled/
ln -s /opt/fjn/beta/conf/nginx/beta_fjn .
ln -s /opt/fjn/www/conf/nginx/www_fjn .
ln -s /opt/fjn/dev/conf/nginx/dev_fjn .
/etc/init.d/nginx restart

# Configurar el supervisor
apt-get install supervisord
/etc/init.d/supervisor stop
cd /etc/supervisor/conf.d/
ln -s /opt/fjn/www/conf/supervisor/fjn_www.conf .
ln -s /opt/fjn/beta/conf/supervisor/fjn_beta.conf .
ln -s /opt/fjn/dev/conf/supervisor/fjn_dev.conf .
/etc/init.d/supervisor start
supervisorctl status

