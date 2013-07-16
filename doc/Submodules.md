# Documentación obtenida de:
# http://www.edy.es/dev/docs/git-guia-rapida/
# http://librosweb.es/pro_git/capitulo_6/submodulos.html
# http://www.huntingbears.com.ve/trabajando-con-submodulos-en-git.html


# Instalar un blog, como un submodulo independiente:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```sh
git submodule add https://github.com/dev-fjn/django-blog-zinnia.git external/django-blog-zinnia
```

# Actualizar los submodulos (el recursivo es opcional)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```sh
git submodule update --init
git submodule update --init --recursive
```


