# Preinstalación 

## Fase I: Instalación del entorno virtual

# Instalación base para iniciar la instalación:

```sh
apt-get install python-virtualenv virtualenvwrapper python-pip git-flow python-dev
```

### Creamos el fichero /etc/profile.d/virtualenvwraper.sh
```bash
#!/bin/sh
# Para virtualenv:
export PROJECT_HOME=${HOME}/Proyectos/Python/
# Preparamos el entorno para virtualenvwrapper:
export WORKON_HOME=${HOME}/.virtualenvs
# Directorio temporal para todas las operaciones
export VIRTUALENVWRAPPER_TMPDIR=/tmp
# Cargamos todo en la sesión:
source /etc/bash_completion.d/virtualenvwrapper
```

> \# Una vez creado este fichero, tendremos que salir de la sesión para recargar los cambios.

## Fase II: Personalizar el entorno

### Directorio de Proyectos:
```sh
cd ${PROJECT_HOME}
git clone git@github.com:dev-fjn/Fundacion.git
```

## Generamos el entorno virtual adecuado:
```sh
mkvirtualenv -a ~/Proyectos/Python/Fundacion --no-site-packages Fundacion

    ó

mkvirtualenv --python=/usr/bin/python3 -a ~/Proyectos/Python/Fundacion --no-site-packages Fundacion
```

## Una vez dentro del  entorno, instalamos Django:
```sh
pip install -r requirements.txt
```

## Ejecutamos git-flow
```sh
git flow init -d
git checkout develop
```

## → a trabajar :)

