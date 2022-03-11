import pytest
import tempfile


@pytest.fixture
def post(user):
    from posts.models import Post
    image = tempfile.NamedTemporaryFile(suffix=".jpg").name
    return Post.objects.create(text='Тестовый пост 1', author=user, image=image)


@pytest.fixture
def group():
    from posts.models import Group
    return Group.objects.create(title='Тестовая группа 1', slug='test-link', description='Тестовое описание группы')


@pytest.fixture
def post_with_group(user, group):
    from posts.models import Post
    image = tempfile.NamedTemporaryFile(suffix=".jpg").name
    return Post.objects.create(text='Тестовый пост 2', author=user, group=group, image=image)


@pytest.fixture
def storage_1():
    from warehouse.models import Storage
    return Storage.objects.create(name='storage_1')


@pytest.fixture
def storage_2():
    from warehouse.models import Storage
    return Storage.objects.create(name='storage_2')


@pytest.fixture
def material():
    from warehouse.models import Material
    return Material.objects.create(name='material')


@pytest.fixture
def instrument():
    from warehouse.models import Instrument
    return Instrument.objects.create(name='instrument')


@pytest.fixture
def material_in_storage_1(material, storage_1):
    from warehouse.models import MaterialStorage
    return MaterialStorage.objects.create(material=material, storage=storage_1, amount=2)


@pytest.fixture
def material_in_storage_2(material, storage_2):
    from warehouse.models import MaterialStorage
    return MaterialStorage.objects.create(material=material, storage=storage_2, amount=4)
