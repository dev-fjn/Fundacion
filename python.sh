#!/bin/bash

# Gestión alternativa de entornos virtuales.

cd $(dirname $0)
test -e ../virtualenv && VIRTUALENV=../virtualenv
test -e virtualenv && VIRTUALENV=virtualenv
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/apps
[ "$VIRTUALENV" ] || exec python $*
source $VIRTUALENV/bin/activate
exec $VIRTUALENV/bin/python $*

