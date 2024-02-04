from ._base import *  # noqa


DATABASES = {
    'default': env.db(),  # noqa (E405)
}
