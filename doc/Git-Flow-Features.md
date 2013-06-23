# Añadir una nueva característica

Para añadir una nueva característica al proyecto, seguiremos este
procedimiento:

 * Entramos en el entorno virtual para ese proyecto
```sh
$ workon Proyecto
```

 * Nos aseguramos, por si acaso, que estamos en la rama develop:
```sh
(Proyecto)usuario@mquina:~/Proyectos/Python/Proyecto$ git branch
* develop
  master
```

A partir de aquí, tenemos dos formas de hacer las cosas:
 * usando git-flow
 * usando git a pelo

## Usemos git-flow

Con git-flow, los pasos a dar son:

 * Comenzamos creando la rama para la nueva característica:
```sh
$ git flow feature start {NOMBRE_RAMA}
```

 * Nos puede interesar subir la nueva rama al repositorio central, para que otros desarrolladores participen en la misma:
```sh
$ git flow feature publish {NOMBRE_RAMA}
```

 * Los demás desarrolladores, para descargarse la nueva rama, harán esto:
```sh
$ git flow feature track {NOMBRE_RAMA}
```

 * Una vez terminado el desarrollo, cerramos la rama de la forma correcta:
```sh
$ git flow feature finish {NOMBRE_RAMA}
```


## Usando git, a pelo

 * Creamos la nueva rama para comenzar a desarrollar en ella la nueva
   caracteristica
```sh
$ git checkout -b {NOMBRE_RAMA} develop
```

 * Subimos la nueva rama a github:
```sh
git push origin {NOMBRE_RAMA}
```


Mientras estemos desarrollando la nueva característica, usaremos la rama {NOMBRE_RAMA}.

Una vez finalizada la tarea, solo tendremos que integrar la rama creada dentro de develop. Para esto usaremos un merge normal y corriente con un parámetro extra, **--no-ff**.

Este flag obliga a Git ha generar un commit para el merge. Con esto se evita que Git haga un fast-forward si es posible (es uno de los métodos para realizar merges, en los que se pierde la historia de la rama).

De esta manera, en todo momento en la historia del repositorio se tendrá constancia de que hubo una rama donde se desarrolló cierta funcionalidad, que commits contenía, y cuando se integró en el trunk.


<center>![Alt "Flujo de trabajo usando git-flow features, usando como ejemplo la corrección de un bug."](http://sysvar.net/static/images/0007-entendiendo-git-flow/feature.png)</center>


 * Volvemos al repositorio develop:
```sh
$ git checkout develop
```

 * Ejecutamos el merge ( con la opcion --no-ff)
```sh
$ git merge --no-ff {NOMBRE_RAMA}
```

 * Podamos la rama (pero no su histórico)
```sh
$ git branch -d {NOMBRE_RAMA}
```

 * Subimos todo al repositorio
```sh
$ git push origin develop
```

Con esto, finalizamos un ciclo de desarrollo para una nueva funcionalidad.

## REFERENCIAS
 * http://sysvar.net/es/usando-git-flow/

