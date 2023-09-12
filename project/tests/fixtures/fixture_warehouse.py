import pytest


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
def material_in_storage_1(material, storage_1, dept_1):
    from warehouse.models import MaterialStorage
    return MaterialStorage.objects.create(material=material, storage=storage_1, amount=2, owner=dept_1)  # noqa (E501)


@pytest.fixture
def material_in_storage_2(material, storage_2, dept_2):
    from warehouse.models import MaterialStorage
    return MaterialStorage.objects.create(material=material, storage=storage_2, amount=4, owner=dept_2)  # noqa (E501)


@pytest.fixture
def component_in_storage_1(component_1, storage_1, dept_1):
    from warehouse.models import ComponentStorage
    return ComponentStorage.objects.create(component=component_1, storage=storage_1, amount=2, owner=dept_1)  # noqa (E501)


@pytest.fixture
def component_in_storage_2(component_2, storage_2, dept_2):
    from warehouse.models import ComponentStorage
    return ComponentStorage.objects.create(component=component_2, storage=storage_2, amount=4, owner=dept_2)  # noqa (E501)
