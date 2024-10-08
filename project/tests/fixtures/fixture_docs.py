import pytest
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def html_file():
    return SimpleUploadedFile(
        'file.html',
        b'file_content',
        content_type='text/plain'
    )


@pytest.fixture
def template(html_file):
    from docs.models import Template
    return Template.objects.create(name='some', file=html_file)


@pytest.fixture
def protocol(template, connection, user, instrument):
    from docs.models import Protocol
    protocol = Protocol.objects.create(
        date='2000-01-01',
        template=template,
        connection=connection,
        supervisor=user,
    )
    protocol.signers.set([user])
    protocol.instruments.set([instrument])
    protocol.save()
    return protocol
