from ._base import *  # noqa

DEBUG = True

DATABASES = {
    'default': env.db(),  # noqa (F405)
}

LOGGING['root']['level'] = 'DEBUG'  # noqa (F405)
