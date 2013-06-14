#!/usr/bin/env python
# -*- coding: utf-8 -*-

# globals

"""

This fabric  file makes  setting up and  deploying a  django application
much easier,  but it  does make  a few  assumptions. Namely  that you're
using Git, Apache and mod_wsgi and your using Debian or Ubuntu. Also you
should have Django installed on your  local machine and SSH installed on
both the local machine and any servers you want to deploy to.

_note  that I've  used the  name project_name  throughout this  example.
Replace this with whatever your project is called._

First step is to create your project locally:

    mkdir project_name
    cd project_name
    django-admin.py startproject project_name

Now  add a  requirements file  so pip  knows to  install Django.  You'll
probably add other  required modules in here later. Creat  a file called
requirements.txt  and  save it  at  the  top  level with  the  following
contents:

    Django

Then save this  fabfile.py file in the top level  directory which should
give you:

    project_name
        fabfile.py
        requirements.txt
        project_name
            __init__.py
            manage.py
            settings.py
            urls.py

You'll need a WSGI file  called project_name.wsgi, where project_name is
the name you gave to your django project. It will probably look like the
following, depending  on your  specific paths and  the location  of your
settings module

    import os
    import sys

    # put the Django project on sys.path
    sys.path.insert(0, \
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

    os.environ["DJANGO_SETTINGS_MODULE"] = "project_name.settings"

    from django.core.handlers.wsgi import WSGIHandler
    application = WSGIHandler()

Last but not least you'll want a virtualhost file for apache which looks
something like  the following.  Save this as  project_name in  the inner
directory. You'll want to  change /path/to/project_name/ to the location
on the remote server you intent to deploy to.

    <VirtualHost *:80>
        WSGIDaemonProcess project_name-production \
            user=project_name group=project_name threads=10 \
            python-path=/path/to/project_name/lib/python2.6/site-packages
        WSGIProcessGroup project_name-production

        WSGIScriptAlias / \
            /path/to/projectname/releases/current/projectname/project_name.wsgi
        <Directory /path/to/project_name/releases/current/project_name>
            Order deny,allow
            Allow from all
        </Directory>

        ErrorLog /var/log/apache2/error.log
        LogLevel warn

        CustomLog /var/log/apache2/access.log combined
    </VirtualHost>

Now  create a  file called  .gitignore, containing  the following.  This
prevents the compiled  python code being included in  the repository and
the archive we use for deployment.

    *.pyc

You should now be ready to initialise  a git repository in the top level
project_name directory.

    git init
    git add .gitignore project_name
    git commit -m "Initial commit"

All of that should leave you with

    project_name
        .git
        .gitignore
        requirements.txt
        fabfile.py
        project_name
            __init__.py
            project_name
            project_name.wsgi
            manage.py
            settings.py
            urls.py

In reality  you might prefer  to keep your  wsgi files and  virtual host
files elsewhere.  The fabfile  has a  variable (env.virtualhost_path)
for this  case. You'll  also want to  set the hosts  that you  intend to
deploy to (env.hosts) as well as the user (env.user).

The first task we're interested in  is called setup. It installs all the
required  software on  the remote  machine, then  deploys your  code and
restarts the webserver.

    fab local setup

After you've made a few changes and commit them to the master Git branch
you can run to deply the changes.

    fab local deploy

If something is wrong then you can rollback to the previous version.

    fab local rollback

Note that  this only allows you  to rollback to the  release immediately
before the latest one. If you want  to pick a arbitrary release then you
can  use the  following,  where  20090727170527 is  a  timestamp for  an
existing release.

    fab local deploy_version:20090727170527

If you want to  ensure your tests run before you  make a deployment then
you can do the following.

    fab local test deploy





Workflow para un deploy con Fabric:

.
└── workflow
    ├── deploy
    │   ├── dev
    │   ├── prod
    │   └── staging
    └── setup
        ├── db
        ├── user
        ├── virtualenv
        └── webserver

"""

from __future__ import with_statement

import os

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.colors import green, red, yellow
from fabric.operations import run
from fabric.context_managers import cd, prefix

# TODO: Reordenar todo este lio en la cabeza y convertirlo en algo práctico.

PROJECT_NAME = 'portal'
REPOS = ((PROJECT_NAME, 'origin', 'master'),)

env.project_name = PROJECT_NAME
env.roledefs = {
    'dev': ['dev.re-cycledair.com'],
    'staging': ['scycledair.com'],
    'prod': ['re-cycledair.com'],
}


########################################################################
# Definición de los Entornos
#######################################################################

def develop():
    '''Faltaba el docstring.'''

    #env.hosts = ['127.0.0.1']
    env.hosts = prompt('IP del host de destino: ')
    print yellow('El host es %s.' % env.hosts)
    #env.user = 'vagrant'
    #env.port = 2222

    # TODO: read from conf file generated by chef

    #env.directory = '/var/www/favouritequestion.com/'
    #env.activate = '/venv/bin/activate'
    #env.git_repo_path = '/var/www/favouritequestion.com/'
    #env.forward_agent = True
    print red('Finalizando develop.')


def server():
    """This pushes to the EC2 instance defined below"""

    # The Elastic IP to your server
    #env.host_string = '999.999.999.999'

    # your user on that system
    #env.user = 'ubuntu'

    # Assumes that your *.pem key is in the same directory as your fabfile.py
    #env.key_filename = 'my_ec2_security_group.pem'

    print red('Finalizando server.')


def staging3():
    '''Faltaba docstring.'''

    #env.hosts = ['54.228.188.132']
    #env.user = 'ec2-user'
    #env.directory = '/srv/www/staging.favouritequestion.com/'

    # TODO: give staging it's own venv (could be created by initialise)

    #env.activate = \
    #    '/home/ec2-user/virtualenv/favouriteQ_staging/env/bin/activate'
    #env.git_repo_path = '/srv/www/git_favouriteQ/'
    #env.key_filename = ['~/.ssh/django.pem']

    # The name supervisor uses
    #env.server_name = 'favourite_q_staging'

    print red('Finalizando staging3.')

########################################################################
# Listado de Funciones
#######################################################################

def build_commit(warn_only=True):
    '''Hacer commit seguro.

Sigue la siguiente lógica:

1) prompt user for the name of the local feature branch you are developing
2) prompt user for the name of the remote branch you want to push your changes
3) to checkout your local feature branch
4) git track add new and modified files
5) prompt user for a commit message
6) run the git commit command with the specified commit message
7) checks out the local copy of the remote branch
8) does a git pull to pull any changes from that remote branch
9) checks out the local feature branch
10) rebases the local feature branch off the recently updated local copy of the remote branch
11) checks out the local copy of the remote branch
12) merges the work from your recently rebased local feature branch into the local copy of the remote branch
13) pushes the local copy of the remote branch to origin
14) checks out the local feature branch so that work can continue
'''

    local_branch = prompt('checkout branch: ')
    rebase_branch = prompt('rebase branch: ')

    #local('git checkout %s' % local_branch)
    #local('git add .')
    #local('git add -u .')

    message = prompt('commit message: ')

    #local('git commit -m "%s"' % message)
    #local('git checkout %s' % rebase_branch)
    #local('git pull origin %s' % rebase_branch)
    #local('git checkout %s' % local_branch)
    #local('git rebase %s' % rebase_branch)
    #local('git checkout %s' % rebase_branch)
    #local('git merge %s' % local_branch)
    #local('git push origin %s' % rebase_branch)
    #local('git checkout %s' % local_branch)
    print red('Finalizando build_commit.')


def collectstatic():
    ''' Fijar los ficheros estáticos. '''

    #with cd(os.path.join(env.directory, PROJECT_NAME)):

    #    # TODO research: with prefix('workon myvenv'):

    #    with prefix('source ' + env.activate):
    #        run('./manage.py collectstatic --noinput')
    print red('Finalizando collectstatic.')


def deploy():
    """
    Deploy the latest version of the site to the servers, install any
    required third party modules, install the virtual host and
    then restart the webserver
    """

    #require('hosts', provided_by=[local])
    #require('path')

    import time
    env.release = time.strftime('%Y%m%d%H%M%S')
    print green(env.release)

    #upload_tar_from_git()
    #install_requirements()
    #install_site()
    #symlink_current_release()
    #migrate()
    #restart_webserver()
    print red('Finalizando deploy.')


def deploy2():
    '''Faltaba el docstring.'''

    # TODO: add a initialise function which sets the project up fresh
    # TODO: do DB backups here
    # TODO: pip update requirements.txt here

    #git_pull()  # could switch branches here

    # could tag the release
    # TODO: research symlinking different versions of the site

    #rsync()
    #install_requirements()

    # TODO: how to stop fixtures running on prod if using them

    #migrate_database()
    #collectstatic()
    #restart_webserver()
    print red('Finalizando deploy2.')

@roles('staging')
def deploy_staging(tag=False):
    '''fab deploy_staging
will deploy the head of the master branch and

    fab deploy_staging:tag=1.0.0
will deploy the 1.0.0 tag.'''

    #code_dir = '/path/to/remote/directory'
    #with cd(code_dir):
    #    run('git fetch')
    #    if tag:
    #        run('git checkout %s' % tag)
    #    else:
    #        run('git checkout master')
    #        run('git pull origin master')

    #    with prefix('source /path/to/virtual/environment/bin/activate'):
    #        run('pip install -r requirements.txt')
    #        run('python manage.py syncdb')
    #        run('python manage.py migrate')
    #        run('python manage.py collectstatic --noinput')
    #        run('touch path/to/wsgi.py')
    print red('Finalizando deploy_staging.')

def deploy_vagrant():
    ''' ... '''

    git_pull()
    install_requirements()
    migrate_database()
    collectstatic()
    restart_apache()
    print red('Finalizando deploy_vagrant.')

def deploy_version(version):
    '''Specify a specific version to be made prod'''

    #require('hosts', provided_by=[local])
    #require('path')

    #env.version = version
    #run('cd $(path); \
    #    rm releases/previous; mv releases/current releases/previous;')
    #run('cd $(path); ln -s $(version) releases/current')
    restart_webserver()
    print red('Finalizando deploy_version.')


def git_pull():
    '''Updates the repository.'''

    #run('cd ~/git/$(repo)/; git pull $(parent) $(branch)')
    print red('Finalizando git_pull.')


def git_pull2():
    '''Updates the repository.'''

    #run('cd ~/git/$(repo)/; git pull $(parent) $(branch)')
    print red('Finalizando git_pull2.')


def git_pull3():
    '''Actualizando el repositorio.'''

    #with cd(env.git_repo_path):

    #    # TODO: take branch or tag as an argument

    #    run('git pull origin master')


    # TODO: also update the config repo (this should be checked out with ssh
    # keys as the GuntOps bit bucket user)
    print red('Finalizando git_pull3.')


def git_reset():
    '''Resets the repository to specified version.'''

    #run('cd ~/git/$(repo)/; git reset --hard $(hash)')
    print red('Finalizando git_reset.')


def git_reset2():
    '''Resets the repository to specified version.'''

    #run('cd ~/git/$(repo)/; git reset --hard $(hash)')
    print red('Finalizando git_pull2.')


def install_requirements():
    '''Install the required packages from the requirements file using pip'''

    #require('release', provided_by=[deploy, setup])
    #run('cd $(path); \
    #    pip install -E . -r ./releases/$(release)/requirements.txt')
    print red('Finalizando requirements.')


def install_requirements2():
    ''' ... '''

    #with cd(os.path.join(env.directory)):
    #    with prefix('source ' + env.activate):
    #        run('pip install -r requirements/requirements.txt')
    #        run('pip install -r requirements/requirements_production.txt')
    print red('Finalizando requirements2.')


def install_site():
    '''Add the virtualhost file to apache'''

    #require('release', provided_by=[deploy, setup])
    #sudo('cd $(path)/releases/$(release); \
    #    cp $(project_name)$(virtualhost_path)$(project_name) \
    #    /etc/apache2/sites-available/')
    #sudo('cd /etc/apache2/sites-available/; a2ensite $(project_name)')
    print red('Finalizando install_site.')


@roles('dev')
def ls_on_dev():
    '''Faltaba el docstring.'''

    #run('ls')  # Runs 'ls' on dev.re-cycledair.com
    print red('Finalizando ls_on_dev.')


@roles('staging')
def ls_on_staging():
    '''Faltaba el docstring.'''

    #run('ls')  # Runs 'ls' on staging.re-cycledair.com
    print red('Finalizando ls_on_staging.')


def migrate():
    '''Update the database'''

    #require('project_name')
    #run('cd $(path)/releases/current/$(project_name); \
    #    ../../../bin/python manage.py syncdb --noinput')
    print red('Finalizando migrate.')


def migrate_database():
    '''Faltaba docstring.'''

    #with cd(os.path.join(env.directory, PROJECT_NAME)):
    #    with prefix('source ' + env.activate):

    #        # Could use fexpect as an alternative
    #        # https://pypi.python.org/pypi/fexpect

    #        run('echo "no\n"| python manage.py syncdb')
    #        run('python manage.py migrate')
    print red('Finalizando migrate_database.')





def pull():
    '''Faltaba el docstring.'''

    #require('fab_hosts', provided_by=[production])

    #for (repo, parent, branch) in env.repos:
    #    env.repo = repo
    #    env.parent = parent
    #    env.branch = branch
    #    # TODO: invoke no es reconocido como comando.
    #    #invoke(git_pull)
    print red('Finalizando pull.')

def reboot2():
    '''Reboot Apache2 server.'''

    #sudo('apache2ctl graceful')
    print red('Finalizando reboot2.')


def restart_apache():
    '''Faltaba docstring.'''

    #sudo('/etc/init.d/apache2 restart')
    print red('Finalizando restart_apache.')


def restart_webserver():
    '''Restart the web server'''

    #sudo('/etc/init.d/apache2 restart')
    print red('Finalizando restart_webserver.')


def restart_webserver2():
    """ Restart Gnunicorn wih Supervisor """

    #sudo('supervisorctl restart ' + env.server_name)
    print red('Finalizando restart_webserver2.')


def rollback():
    """
    Limited rollback capability. Simple loads the previously current
    version of the code. Rolling back again will swap between the two.
    """

    #require('hosts', provided_by=[local])
    #require('path')

    #run('cd $(path); mv releases/current releases/_previous;')
    #run('cd $(path); mv releases/previous releases/current;')
    #run('cd $(path); mv releases/_previous releases/previous;')
    #restart_webserver()
    print red('Finalizando rollback.')


def rsync():
    '''Faltaba docstring.'''

    #run('rsync -av --delete --exclude .git* --exclude localsettings.py '
    #     + env.git_repo_path + ' ' + env.directory)
    print red('Finalizando rsync.')


def setup():
    """
    Setup a fresh virtualenv as well as a few useful directories, then run
    a full deployment
    """

    #require('hosts', provided_by=[local])
    #require('path')

    #sudo('aptitude install -y python-setuptools')
    #sudo('easy_install pip')
    #sudo('pip install virtualenv')
    #sudo('aptitude install -y apache2')
    #sudo('aptitude install -y libapache2-mod-wsgi')

    # we want rid of the defult apache config

    #sudo('cd /etc/apache2/sites-available/; a2dissite default;')
    #run('mkdir -p $(path); cd $(path); virtualenv .;')
    # TODO: revisar el uso de la opción fail en este comando.
    #run('cd $(path); mkdir releases; mkdir shared; mkdir packages;',
    #    fail='ignore')
    #deploy()
    print red('Finalizando setup.')


def staging():
    '''Faltaba el docstring.'''

    #env.fab_hosts = ['a.staging_example.com']
    #env.repos = REPOS
    print red('Finalizando staging.')



# tasks

# Helpers. These are called by other functions rather than directly

## http://lethain.com/deploying-django-with-fabric/

## http://www.yaconiello.com/blog/ \
##    deploying-django-site-fabric/#sthash.Yl5n8ExY.LZsro5zM.dpbs

def staging2():
    ''' Staging detallado.'''

    # path to the directory on the server where your vhost is set up
    #server_path = '/home/ubuntu/www/dev.yaconiello.com'

    # name of the application process
    #process = 'staging'

    print red('Beginning Deploy:')

    #with cd('%s/app' % server_path):

    #    run('pwd')

    #    print green('Pulling master from GitHub...')
    #    run('git pull origin master')

    #    print green('Installing requirements...')
    #    run('source %s/venv/bin/activate && pip install -r requirements.txt'
    #         % server_path)

    #    print green('Collecting static files...')
    #    run("source %s/venv/bin/activate && python manage.py collectstatic \
    #        --noinput"
    #         % server_path)

    #    print green('Syncing the database...')
    #    run('source %s/venv/bin/activate && python manage.py syncdb'
    #        % server_path)

    #    print green('Migrating the database...')
    #    run('source %s/venv/bin/activate && python manage.py migrate'
    #        % server_path)

    #    print green('Restart the uwsgi process')
    #    run('sudo service %s restart' % process)

    print red('Finalizando staging2.')

## http://www.re-cycledair.com/deploying-django-with-fabric

def symlink_current_release():
    '''Symlink our current release'''

    #require('release', provided_by=[deploy, setup])

    # TODO: Revisar el uso del parámetro fail en esta orden.

    #run('cd $(path); \
    #    rm releases/previous; \
    #    mv releases/current releases/previous;', fail='ignore')
    #run('cd $(path); ln -s $(release) releases/current')

    print red('Finalizando symlink_current_release.')


def test():
    '''Run the test suite and bail out if it fails.

Hay un aviso sobre el parámetro fail. Revisarlo.'''

    #local('cd $(project_name); python manage.py test', fail='abort')

    print red('Finalizando test.')


def test2():
    '''Faltaba el docstring.'''

    # TODO: revisar el uso de fail en esta línea.
    #local('python manage.py test', fail='abort')

    print red('Finalizando test2.')


def upload_tar_from_git():
    '''Faltaba docstring.'''

    #require('release', provided_by=[deploy, setup])

    #local('git archive --format=tar master | gzip > $(release).tar.gz')
    #run('mkdir $(path)/releases/$(release)')
    #put('$(release).tar.gz', '$(path)/packages/')
    #run('cd $(path)/releases/$(release); \
    #    tar zxf ../../packages/$(release).tar.gz')
    #local('rm $(release).tar.gz')

    print red('Finalizando upload_tar_from_git.')


# def syncdb():
#     with cd(SERVER_PATH):
#         run('python manage.py syncdb')

# def deploy():
#     # Remove all .pyc files
#     local("find . -name \*.pyc -delete")
#     local("tar -czvf /tmp/pricedag.tar.gz * --exclude=database.db \
#                                             --exclude=fabfile.py \
#                                             --exclude=.project \
#                                             --exclude=.pydevproject")

#     put("/tmp/pricedag.tar.gz", "/tmp/")
#     run("rm -rf %s %s" % SERVER_PATH)
#     run("mkdir -p %s" % SERVER_PATH)
#     run("tar -zxvf /tmp/pricedag.tar.gz -C %s" % SERVER_PATH)
#     run("tar -zxvf /tmp/pricedag.tar.gz -C %s" % SERVER_PATH)
#     restart_webserver()
#     syncdb()

# def git_pull():
#     "Updates the repository."
#     run("cd ~/git/$(repo)/; git pull $(parent) $(branch)")

# def git_reset():
#     "Resets the repository to specified version."
#     run("cd ~/git/$(repo)/; git reset --hard $(hash)")

    print red('Finalizando upload_tar_from_git.')
