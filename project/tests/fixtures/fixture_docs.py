import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from docs.models import Integer, File, Float, Text


@pytest.fixture(scope='session')
def html_file():
    return SimpleUploadedFile('file.html', b'file_content')


@pytest.fixture(scope='session')
def image_file():
    return SimpleUploadedFile('image.png', b'file_content', 'image/png')


@pytest.fixture
def template(html_file):
    from docs.models import Template
    return Template.objects.create(name='some', file=html_file)


@pytest.fixture
def protocol(template, hardware, user, instrument):
    from docs.models import Protocol
    protocol = Protocol.objects.create(
        date='2000-01-01',
        template=template,
        hardware=hardware,
        supervisor=user,
    )
    protocol.signers.set([user])
    protocol.instruments.set([instrument])
    protocol.save()
    return protocol


@pytest.fixture
def image(protocol, image_file):
    return File.objects.create(
        slug='slug', protocol=protocol, value=image_file
    )


@pytest.fixture
def integer(protocol):
    return Integer.objects.create(slug='slug', protocol=protocol, value=12)


@pytest.fixture
def float_(protocol):
    return Float.objects.create(slug='slug', protocol=protocol, value=12.2)


@pytest.fixture
def text(protocol):
    return Text.objects.create(slug='slug', protocol=protocol, value='bar')


@pytest.fixture
def char(protocol):
    return Text.objects.create(slug='some-slug', protocol=protocol, value='foo')
