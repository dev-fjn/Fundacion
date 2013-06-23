# Git Flow
## Uso diario

### Resumen visual de los comandos usados en Git-flow
<center>![Alt "Esquema de comandos usados en Git Flow"](http://danielkummer.github.io/git-flow-cheatsheet/img/git-flow-commands.png "Esquema de comandos usados en Git Flow")</center>


##Funciones de las ramas

###Rama Master
Cada commit indica una nueva versión del proyecto.

>Se crea a partir de: -

>Se integra en: -

###Rama Develop
Contiene el desarrollo del proyecto

>Se crea a partir de: -

>Se integra en: -

###Rama Feature
Cada rama contiene el desarrollo de una funcionalidad.

>Se crea a partir de: develop

>Se integra en: develop

###Rama Release (release-XXX)
Se realiza el trabajo necesario para lanzar una nueva versión.

>Se crea a partir de: develop

>Se integra en: develop y master

###Rama Hotfix (hotfix-XXX)
Se corrige un fallo urgente.

>Se crea a partir de: master

>Se integra en: develop y master

#Ilustración del flujo de trabajo con Git-Flow
<center>![Alt "Esquema de comandos usados en Git Flow"] (https://community.jboss.org/servlet/JiveServlet/showImage/16474/RichFacesWorkflow.png) "Flujo de trabajo usando git-flow"</center>

#Referencias
  * http://jesuslc.com/2013/04/28/cheat-sheet-sobre-git-flow-chuletaresumen/
  * http://sysvar.net/es/entendiendo-git-flow/
  * http://sysvar.net/es/usando-git-flow/
  * http://codeloveandboards.com/blog/2013/04/06/automatiza-tu-manera-de-usar-git-con-git-flow/

