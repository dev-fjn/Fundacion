
cd ${PROJECT_HOME}

git clone git@github.com:lcabrera/Fundacion.git

workon Fundacion

git flow init -d

git branch --set-upstream-to=origin/develop develop

git pull

./manage.py syncdb

./manage.py schemamigration debug_toolbar --initial


