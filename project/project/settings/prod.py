from ._base import *  # noqa


DATABASES = {
    'default': env.db(),
}
