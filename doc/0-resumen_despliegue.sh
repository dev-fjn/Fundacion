#!/bin/sh -x

adduser fjn_beta --disabled-password
adduser fjn_prod --disabled-password
adduser fjn_dev --disabled-password

# Crear las carpetas para el static y el media en /var/www/fjn/

cd /var/www/
mkdir -p fjn_beta/static fjn_beta/media
mkdir -p fjn_dev/static fjn_dev/media
mkdir -p fjn_prod/static fjn_prod/media
chown -R fjn_beta fjn_beta
chown -R fjn_dev fjn_dev
chown -R fjn_prod fjn_prod 

# Crear base de datos para produccion beta y dev

su - postgres
createuser fjn_prod --no-superuser --no-createrole --no-createdb --password
createdb fjn_prod --owner fjn_prod
createuser fjn_beta --no-superuser --no-createrole --no-createdb --password
createdb fjn_beta --owner fjn_beta
createuser fjn_dev --no-superuser --no-createrole --no-createdb --password
createdb fjn_dev --owner fjn_dev
exit

# clonar cada uno de los despliegues en /opt/fjn/

test -d /home/fjn_dev || git clone git@github.com:dev-fjn/Fundacion.git /home/fjn_dev/Fundacion
cd /home/fjn_dev/Fundacion
git checkout develop
echo "DEBUG = True" > portal/settings.d/000.STATUS.py
echo "PRODUCCION = False" >> portal/settings.d/000.STATUS.py
bash -x doc/0-resumen_instalacion.sh

test -d /home/fjn_beta || git clone git@github.com:dev-fjn/Fundacion.git /home/fjn_beta/Fundacion
cd /home/fjn_beta/Fundacion
git checkout master
echo "DEBUG = True" > portal/settings.d/000.STATUS.py
echo "PRODUCCION = True" >> portal/settings.d/000.STATUS.py
bash -x doc/0-resumen_instalacion.sh

test -d /home/fjn_prod || git clone git@github.com:dev-fjn/Fundacion.git /home/fjn_prod/Fundacion
cd /home/fjn_prod/Fundacion
git checkout master
echo "DEBUG = True" > portal/settings.d/000.STATUS.py
echo "PRODUCCION = False" >> portal/settings.d/000.STATUS.py
bash -x doc/0-resumen_instalacion.sh

# Configurar el nginx

cd /etc/nginx/sites-enabled/
ln -s /opt/fjn/beta/conf/nginx/beta_fjn .
ln -s /opt/fjn/prod/conf/nginx/prod_fjn .
ln -s /opt/fjn/dev/conf/nginx/dev_fjn .
/etc/init.d/nginx restart

# Configurar el supervisor
apt-get install supervisord
/etc/init.d/supervisor stop
cd /etc/supervisor/conf.d/
ln -s /opt/fjn/prod/conf/supervisor/fjn_prod.conf .
ln -s /opt/fjn/beta/conf/supervisor/fjn_beta.conf .
ln -s /opt/fjn/dev/conf/supervisor/fjn_dev.conf .
/etc/init.d/supervisor start
supervisorctl status

