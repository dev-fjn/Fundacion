# Git

Después de ejecutar git flow init, subimos la rama develop a github
```sh
git push origin develop
```

Fijar tanto la rama develop, en los dos extremos, como rama por defecto:
```sh
git branch --set-upstream-to=origin/develop develop
```
