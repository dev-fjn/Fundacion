# -*- coding: utf-8 -*-

'''Usar las cabeceras de proxy

El nginx haciendo como proxy inverso pone las cabecesras X-Forwarded-Host para referirse
al host que el cliente pide realmente. Pues este setting es para confiar en ello
'''

if PRODUCCION:
    USE_X_FORWARDED_HOST = True
