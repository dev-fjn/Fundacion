# -*- coding: utf-8 -*-

'''Activar la barra de depuración.

'''

if DEBUG and not PRODUCCION:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
    INSTALLED_APPS += (
        'debug_toolbar',
        'debug_toolbar_htmltidy',
        'debug_toolbar_user_panel',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
    INTERNAL_IPS = ('127.0.0.1', )
    DEBUG_TOOLBAR_PANELS = (
            'debug_toolbar.panels.timer.TimerDebugPanel',
            'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
            'debug_toolbar.panels.headers.HeaderDebugPanel',
            'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
            'debug_toolbar.panels.template.TemplateDebugPanel',
            'debug_toolbar.panels.sql.SQLDebugPanel',
            'debug_toolbar.panels.signals.SignalDebugPanel',
            'debug_toolbar.panels.logger.LoggingPanel',
            'debug_toolbar.panels.version.VersionDebugPanel',

            # debug_toolbar_extra
            'debug_toolbar_extra.panels.PrintTemplateNamePanel',

            # debug_toolbar_htmltidy
            'debug_toolbar_htmltidy.panels.HTMLTidyDebugPanel',

            # debug_toolbar_user_panel
            'debug_toolbar_user_panel.panels.UserPanel',
    )

    def custom_show_toolbar(request):
        '''If True, always show toolbar, for example purposes only.'''
        return False

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    #    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar, # Peta la barra de depuración
    #    'EXTRA_SIGNALS': ['myproject.signals.MySignal'], # Peta: habría que definir las señales a usar.
        'HIDE_DJANGO_SQL': False,
        'TAG': 'div',
        'ENABLE_STACKTRACES' : True,
    }

