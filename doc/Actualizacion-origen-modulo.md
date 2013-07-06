# Leido de:
# https://help.github.com/articles/fork-a-repo
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

f
cd PROYECTO
git remote add upstream https://github.com/smcoll/django-scheduler.git

fjn-dev@elsa:~/Proyectos/Python/django-scheduler$ git remote 
origin
upstream


fjn-dev@elsa:~/Proyectos/Python/django-scheduler$ git fetch upstream
De https://github.com/smcoll/django-scheduler
* [new branch]      add-tags   -> upstream/add-tags
* [new branch]      ajax_ui    -> upstream/ajax_ui
* [new branch]      develop    -> upstream/develop
* [new branch]      feature/100_percente_coverage -> upstream/feature/100_percente_coverage
  [new branch]      feature/django_1_5_migration -> upstream/feature/django_1_5_migration
* [new branch]      fix-calendar-views-tz-support -> upstream/fix-calendar-views-tz-support
* [new branch]      fix-period-tz-support -> upstream/fix-period-tz-support
* [new branch]      master     -> upstream/master
* [new branch]      seo-calendar-urls -> upstream/seo-calendar-urls
* [new branch]      timely     -> upstream/timely


fjn-dev@elsa:~/Proyectos/Python/django-scheduler$ git fetch upstream master
De https://github.com/smcoll/django-scheduler
* branch            master     -> FETCH_HEAD

fjn-dev@elsa:~/Proyectos/Python/django-scheduler$ git merge upstream/master

