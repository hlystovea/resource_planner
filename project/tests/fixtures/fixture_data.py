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


@pytest.fixture
def function():
    from hardware.models import ComponentFunction
    return ComponentFunction.objects.create(name='function')


@pytest.fixture
def design():
    from hardware.models import ComponentDesign
    return ComponentDesign.objects.create(name='design', abbreviation='d')


@pytest.fixture
def repair_method():
    from hardware.models import ComponentRepairMethod
    return ComponentRepairMethod.objects.create(name='repair_method')


@pytest.fixture
def facility():
    from hardware.models import Facility
    return Facility.objects.create(
        name='facility',
        abbreviation='f'
    )


@pytest.fixture
def connection(facility):
    from hardware.models import Connection
    return Connection.objects.create(
        name='connection',
        abbreviation='c',
        facility=facility
    )


@pytest.fixture
def group():
    from hardware.models import Group
    return Group.objects.create(
        name='group',
        abbreviation='g'
    )


@pytest.fixture
def hardware(connection, group):
    from hardware.models import Hardware
    return Hardware.objects.create(
        name='hardware',
        inventory_number='007',
        connection=connection,
        group=group
    )


@pytest.fixture
def cabinet(hardware):
    from hardware.models import Cabinet
    return Cabinet.objects.create(
        name='cabinet',
        abbreviation='c',
        hardware=hardware,
        manufacturer='manufacturer',
        release_year=2000,
        launch_year=2000
    )


@pytest.fixture
def component(function, design, repair_method, cabinet):
    from hardware.models import Component
    return Component.objects.create(
        name='component',
        function=function,
        design=design,
        manufacturer='manufacturer',
        release_year=2000,
        launch_year=2000,
        repair_method=repair_method,
        cabinet=cabinet
    )


@pytest.fixture
def effect():
    from defects.models import Effect
    return Effect.objects.create(name='effect')

@pytest.fixture
def condition():
    from defects.models import Condition
    return Condition.objects.create(name='condition')

@pytest.fixture
def feature():
    from defects.models import Feature
    return Feature.objects.create(name='feature')

@pytest.fixture
def technical_reason():
    from defects.models import TechnicalReason
    return TechnicalReason.objects.create(name='technical_reason')

@pytest.fixture
def organizational_reason():
    from defects.models import OrganizationalReason
    return OrganizationalReason.objects.create(name='organizational_reason')

@pytest.fixture
def defect(component, user, effect, feature, condition):
    from defects.models import Defect
    defect = Defect(
        date='2000-01-01',
        component=component,
        employee=user,
        description='Описание дефекта',
        condition=condition
    )
    defect.save()
    defect.effects.set([effect])
    defect.features.set([feature])
    return defect