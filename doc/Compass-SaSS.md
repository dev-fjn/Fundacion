# Breve introducción:
# ~~~~~~~~~~~~~~~~~~~
# http://dzignus.github.io/workshop-sass-compass/#1

# Debian
apt-get install ruby
apt-get install rubygems

# Instalamos paquetería:
# ~~~~~~~~~~~~~~~~~~~~~~
gem install sass compass susy compass-recipes

# Crear la base:
# ~~~~~~~~~~~~~
cd ~/Proyectos/Python/Fundacion/portada/
compass create static -r susy -u susy

# ponerla en escucha:
# ~~~~~~~~~~~~~~~~~~
cd ~/Proyectos/Python/Fundacion/portada/static
clear && compass watch .
