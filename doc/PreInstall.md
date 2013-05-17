# Preinstalación 

## Fase I: Instalación del entorno virtual
><pre><code>apt-get install python-virtualenv virtualenvwrapper python-pip
apt-get install git-flow</code></pre>

```sh
apt-get install python-virtualenv virtualenvwrapper python-pip
apt-get install git-flow
```

### Creamos el fichero /etc/profile.d/virtualenvwraper.sh
><pre><code>
>\## ---- 8< --------------------------------------------- ##
>\#!/bin/sh
>\# Para virtualenv:
>export PROJECT_HOME=${HOME}/Proyectos/Python/
>\# Preparamos el entorno para virtualenvwrapper:
>export WORKON_HOME=${HOME}/.virtualenvs
>\# Directorio temporal para todas las operaciones
>export VIRTUALENVWRAPPER_TMPDIR=/tmp
>\# Cargamos todo en la sesión:
>source /etc/bash_completion.d/virtualenvwrapper
>\## ---- >8 --------------------------------------------- ##</code></pre>

> \# Una vez creado este fichero, tendremos que salir de la sesión para recargar los cambios.

## Fase II: Personalizar el entorno

### Directorio de Proyectos:
><pre><code>cd ${PROJECT_HOME}
>git clone git@github.com:dev-fjn/Fundacion.git</code></pre>

## Generamos el entorno virtual adecuado:
><pre><code>mkvirtualenv -a ~/Proyectos/Python/Fundacion --no-site-packages Fundacion</code></pre>

## Una vez dentro del  entorno, instalamos Django:
><pre><code>pip install -r requirements.txt</code></pre>

## Ejecutamos git-flow
><pre><code>git-flow init -d
git checkout develop</code></pre>

## → a trabajar :)

